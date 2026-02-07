-- ============================================
-- Email Campaign Database Schema
-- PostgreSQL 12+
-- ============================================

-- ============================================
-- 1. Recipients Table
-- ============================================
CREATE TABLE IF NOT EXISTS recipients (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    full_name VARCHAR(200) GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED,
    language VARCHAR(10) DEFAULT 'en',
    segment VARCHAR(50),
    subscribed BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    phone VARCHAR(50),
    country VARCHAR(100),
    city VARCHAR(100),
    company VARCHAR(200),
    job_title VARCHAR(100),
    
    -- Metadata
    source VARCHAR(100), -- откуда пришел (website, api, import, etc.)
    tags TEXT[], -- массив тегов
    custom_fields JSONB, -- дополнительные поля
    
    -- Timestamps
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    unsubscribed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_email_sent_at TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT valid_language CHECK (language IN ('en', 'ru', 'es', 'de', 'fr', 'it', 'pt', 'zh', 'ja'))
);

-- Indexes for recipients
CREATE INDEX idx_recipients_email ON recipients(email);
CREATE INDEX idx_recipients_subscribed ON recipients(subscribed);
CREATE INDEX idx_recipients_segment ON recipients(segment);
CREATE INDEX idx_recipients_language ON recipients(language);
CREATE INDEX idx_recipients_tags ON recipients USING GIN(tags);
CREATE INDEX idx_recipients_custom_fields ON recipients USING GIN(custom_fields);

-- Trigger to update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_recipients_updated_at BEFORE UPDATE ON recipients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 2. Campaigns Table
-- ============================================
CREATE TABLE IF NOT EXISTS campaigns (
    id SERIAL PRIMARY KEY,
    campaign_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL, -- newsletter, promotional, transactional, triggered
    status VARCHAR(50) DEFAULT 'draft', -- draft, scheduled, sending, sent, paused, cancelled
    
    -- Targeting
    segment VARCHAR(50),
    language VARCHAR(10),
    recipient_count INTEGER DEFAULT 0,
    
    -- Email content
    subject_line VARCHAR(500),
    preview_text VARCHAR(200),
    from_email VARCHAR(255),
    from_name VARCHAR(100),
    reply_to VARCHAR(255),
    
    -- Templates
    template_id VARCHAR(100),
    html_template TEXT,
    text_template TEXT,
    
    -- Scheduling
    scheduled_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- A/B Testing
    ab_test_enabled BOOLEAN DEFAULT false,
    ab_test_variant VARCHAR(10), -- A, B, C, etc.
    ab_test_percentage INTEGER, -- процент для каждого варианта
    
    -- Settings
    track_opens BOOLEAN DEFAULT true,
    track_clicks BOOLEAN DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    
    CONSTRAINT valid_type CHECK (type IN ('newsletter', 'promotional', 'transactional', 'triggered', 'welcome', 'abandoned_cart')),
    CONSTRAINT valid_status CHECK (status IN ('draft', 'scheduled', 'sending', 'sent', 'paused', 'cancelled'))
);

CREATE INDEX idx_campaigns_campaign_id ON campaigns(campaign_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_type ON campaigns(type);
CREATE INDEX idx_campaigns_scheduled_at ON campaigns(scheduled_at);

CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 3. Email Logs Table
-- ============================================
CREATE TABLE IF NOT EXISTS email_logs (
    id SERIAL PRIMARY KEY,
    campaign_id VARCHAR(100),
    recipient_id INTEGER REFERENCES recipients(id),
    email VARCHAR(255) NOT NULL,
    
    -- Email details
    subject VARCHAR(500),
    from_email VARCHAR(255),
    
    -- Status
    status VARCHAR(50) NOT NULL, -- queued, sent, delivered, bounced, failed, rejected
    provider VARCHAR(50), -- smtp, sendgrid, mailgun, gmail, ses
    provider_message_id VARCHAR(255),
    
    -- Error handling
    error_code VARCHAR(50),
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Timestamps
    queued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    
    -- Metadata
    ip_address INET,
    user_agent TEXT,
    metadata JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_status CHECK (status IN ('queued', 'sent', 'delivered', 'bounced', 'failed', 'rejected', 'deferred'))
);

CREATE INDEX idx_email_logs_campaign_id ON email_logs(campaign_id);
CREATE INDEX idx_email_logs_recipient_id ON email_logs(recipient_id);
CREATE INDEX idx_email_logs_email ON email_logs(email);
CREATE INDEX idx_email_logs_status ON email_logs(status);
CREATE INDEX idx_email_logs_sent_at ON email_logs(sent_at);
CREATE INDEX idx_email_logs_provider ON email_logs(provider);

-- ============================================
-- 4. Email Events Table (opens, clicks, etc.)
-- ============================================
CREATE TABLE IF NOT EXISTS email_events (
    id SERIAL PRIMARY KEY,
    email_log_id INTEGER REFERENCES email_logs(id),
    campaign_id VARCHAR(100),
    recipient_id INTEGER REFERENCES recipients(id),
    email VARCHAR(255) NOT NULL,
    
    -- Event details
    event_type VARCHAR(50) NOT NULL, -- open, click, bounce, spam_report, unsubscribe
    event_data JSONB,
    
    -- For clicks
    url TEXT,
    link_name VARCHAR(255),
    
    -- For bounces
    bounce_type VARCHAR(50), -- hard, soft, block
    bounce_reason TEXT,
    
    -- Device/Location info
    ip_address INET,
    user_agent TEXT,
    device_type VARCHAR(50), -- desktop, mobile, tablet
    browser VARCHAR(100),
    os VARCHAR(100),
    country VARCHAR(100),
    city VARCHAR(100),
    
    -- Timestamp
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_event_type CHECK (event_type IN ('open', 'click', 'bounce', 'spam_report', 'unsubscribe', 'delivered', 'deferred', 'dropped'))
);

CREATE INDEX idx_email_events_email_log_id ON email_events(email_log_id);
CREATE INDEX idx_email_events_campaign_id ON email_events(campaign_id);
CREATE INDEX idx_email_events_recipient_id ON email_events(recipient_id);
CREATE INDEX idx_email_events_event_type ON email_events(event_type);
CREATE INDEX idx_email_events_timestamp ON email_events(event_timestamp);

-- ============================================
-- 5. Unsubscribe List
-- ============================================
CREATE TABLE IF NOT EXISTS unsubscribes (
    id SERIAL PRIMARY KEY,
    recipient_id INTEGER REFERENCES recipients(id),
    email VARCHAR(255) NOT NULL,
    
    -- Unsubscribe details
    reason VARCHAR(255),
    reason_text TEXT,
    campaign_id VARCHAR(100),
    
    -- Source
    unsubscribe_method VARCHAR(50), -- link, reply, manual, complaint
    ip_address INET,
    user_agent TEXT,
    
    -- Timestamps
    unsubscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_unsubscribe_method CHECK (unsubscribe_method IN ('link', 'reply', 'manual', 'complaint', 'bounce'))
);

CREATE INDEX idx_unsubscribes_email ON unsubscribes(email);
CREATE INDEX idx_unsubscribes_recipient_id ON unsubscribes(recipient_id);
CREATE INDEX idx_unsubscribes_campaign_id ON unsubscribes(campaign_id);

-- ============================================
-- 6. Bounce List
-- ============================================
CREATE TABLE IF NOT EXISTS bounces (
    id SERIAL PRIMARY KEY,
    recipient_id INTEGER REFERENCES recipients(id),
    email VARCHAR(255) NOT NULL,
    
    -- Bounce details
    bounce_type VARCHAR(50) NOT NULL, -- hard, soft, block
    bounce_reason TEXT,
    bounce_code VARCHAR(50),
    campaign_id VARCHAR(100),
    
    -- Provider info
    provider VARCHAR(50),
    provider_response TEXT,
    
    -- Timestamps
    bounced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_bounce_type CHECK (bounce_type IN ('hard', 'soft', 'block', 'undetermined'))
);

CREATE INDEX idx_bounces_email ON bounces(email);
CREATE INDEX idx_bounces_recipient_id ON bounces(recipient_id);
CREATE INDEX idx_bounces_bounce_type ON bounces(bounce_type);

-- ============================================
-- 7. Suppression List (combined blacklist)
-- ============================================
CREATE TABLE IF NOT EXISTS suppressions (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    
    -- Suppression details
    reason VARCHAR(50) NOT NULL, -- bounce, complaint, unsubscribe, manual
    description TEXT,
    
    -- Timestamps
    suppressed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP, -- для временных блокировок
    
    CONSTRAINT valid_reason CHECK (reason IN ('bounce', 'complaint', 'unsubscribe', 'manual', 'invalid', 'role_based'))
);

CREATE INDEX idx_suppressions_email ON suppressions(email);
CREATE INDEX idx_suppressions_reason ON suppressions(reason);

-- ============================================
-- 8. Campaign Statistics (aggregated)
-- ============================================
CREATE TABLE IF NOT EXISTS campaign_stats (
    id SERIAL PRIMARY KEY,
    campaign_id VARCHAR(100) UNIQUE NOT NULL,
    
    -- Sending stats
    total_recipients INTEGER DEFAULT 0,
    total_sent INTEGER DEFAULT 0,
    total_delivered INTEGER DEFAULT 0,
    total_bounced INTEGER DEFAULT 0,
    total_failed INTEGER DEFAULT 0,
    
    -- Engagement stats
    total_opens INTEGER DEFAULT 0,
    unique_opens INTEGER DEFAULT 0,
    total_clicks INTEGER DEFAULT 0,
    unique_clicks INTEGER DEFAULT 0,
    
    -- Negative stats
    total_unsubscribes INTEGER DEFAULT 0,
    total_spam_reports INTEGER DEFAULT 0,
    
    -- Calculated rates
    delivery_rate DECIMAL(5,2),
    open_rate DECIMAL(5,2),
    click_rate DECIMAL(5,2),
    bounce_rate DECIMAL(5,2),
    unsubscribe_rate DECIMAL(5,2),
    
    -- Timestamps
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_campaign_stats_campaign_id ON campaign_stats(campaign_id);

-- ============================================
-- 9. Email Templates
-- ============================================
CREATE TABLE IF NOT EXISTS email_templates (
    id SERIAL PRIMARY KEY,
    template_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Template content
    subject_line VARCHAR(500),
    html_content TEXT,
    text_content TEXT,
    
    -- Metadata
    language VARCHAR(10),
    category VARCHAR(50), -- welcome, newsletter, promotional, transactional
    tags TEXT[],
    
    -- Version control
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100)
);

CREATE INDEX idx_email_templates_template_id ON email_templates(template_id);
CREATE INDEX idx_email_templates_category ON email_templates(category);
CREATE INDEX idx_email_templates_language ON email_templates(language);

CREATE TRIGGER update_email_templates_updated_at BEFORE UPDATE ON email_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 10. A/B Test Results
-- ============================================
CREATE TABLE IF NOT EXISTS ab_test_results (
    id SERIAL PRIMARY KEY,
    campaign_id VARCHAR(100) NOT NULL,
    variant VARCHAR(10) NOT NULL, -- A, B, C, etc.
    
    -- Stats per variant
    sent_count INTEGER DEFAULT 0,
    delivered_count INTEGER DEFAULT 0,
    open_count INTEGER DEFAULT 0,
    click_count INTEGER DEFAULT 0,
    unsubscribe_count INTEGER DEFAULT 0,
    
    -- Calculated rates
    open_rate DECIMAL(5,2),
    click_rate DECIMAL(5,2),
    
    -- Winner determination
    is_winner BOOLEAN DEFAULT false,
    confidence_level DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ab_test_results_campaign_id ON ab_test_results(campaign_id);

-- ============================================
-- Views for Analytics
-- ============================================

-- View: Recent campaign performance
CREATE OR REPLACE VIEW v_campaign_performance AS
SELECT 
    c.campaign_id,
    c.name,
    c.type,
    c.status,
    c.scheduled_at,
    c.completed_at,
    cs.total_sent,
    cs.total_delivered,
    cs.delivery_rate,
    cs.unique_opens,
    cs.open_rate,
    cs.unique_clicks,
    cs.click_rate,
    cs.total_unsubscribes,
    cs.unsubscribe_rate
FROM campaigns c
LEFT JOIN campaign_stats cs ON c.campaign_id = cs.campaign_id
ORDER BY c.created_at DESC;

-- View: Recipient engagement
CREATE OR REPLACE VIEW v_recipient_engagement AS
SELECT 
    r.id,
    r.email,
    r.full_name,
    r.segment,
    COUNT(DISTINCT el.id) as emails_received,
    COUNT(DISTINCT CASE WHEN ee.event_type = 'open' THEN ee.id END) as total_opens,
    COUNT(DISTINCT CASE WHEN ee.event_type = 'click' THEN ee.id END) as total_clicks,
    MAX(el.sent_at) as last_email_date,
    CASE 
        WHEN MAX(el.sent_at) < CURRENT_TIMESTAMP - INTERVAL '90 days' THEN 'inactive'
        WHEN MAX(el.sent_at) < CURRENT_TIMESTAMP - INTERVAL '30 days' THEN 'at_risk'
        ELSE 'active'
    END as engagement_status
FROM recipients r
LEFT JOIN email_logs el ON r.id = el.recipient_id
LEFT JOIN email_events ee ON el.id = ee.email_log_id
WHERE r.subscribed = true
GROUP BY r.id, r.email, r.full_name, r.segment;

-- View: Daily email volume
CREATE OR REPLACE VIEW v_daily_email_volume AS
SELECT 
    DATE(sent_at) as send_date,
    COUNT(*) as total_sent,
    COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered,
    COUNT(CASE WHEN status = 'bounced' THEN 1 END) as bounced,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed,
    ROUND(COUNT(CASE WHEN status = 'delivered' THEN 1 END)::NUMERIC / COUNT(*)::NUMERIC * 100, 2) as delivery_rate
FROM email_logs
WHERE sent_at IS NOT NULL
GROUP BY DATE(sent_at)
ORDER BY send_date DESC;

-- ============================================
-- Stored Procedures
-- ============================================

-- Procedure: Update campaign statistics
CREATE OR REPLACE FUNCTION update_campaign_stats(p_campaign_id VARCHAR)
RETURNS VOID AS $$
BEGIN
    INSERT INTO campaign_stats (
        campaign_id,
        total_recipients,
        total_sent,
        total_delivered,
        total_bounced,
        total_failed,
        total_opens,
        unique_opens,
        total_clicks,
        unique_clicks,
        total_unsubscribes,
        total_spam_reports,
        delivery_rate,
        open_rate,
        click_rate,
        bounce_rate,
        unsubscribe_rate,
        last_updated
    )
    SELECT 
        p_campaign_id,
        COUNT(DISTINCT el.recipient_id),
        COUNT(CASE WHEN el.status IN ('sent', 'delivered') THEN 1 END),
        COUNT(CASE WHEN el.status = 'delivered' THEN 1 END),
        COUNT(CASE WHEN el.status = 'bounced' THEN 1 END),
        COUNT(CASE WHEN el.status = 'failed' THEN 1 END),
        COUNT(CASE WHEN ee.event_type = 'open' THEN 1 END),
        COUNT(DISTINCT CASE WHEN ee.event_type = 'open' THEN ee.recipient_id END),
        COUNT(CASE WHEN ee.event_type = 'click' THEN 1 END),
        COUNT(DISTINCT CASE WHEN ee.event_type = 'click' THEN ee.recipient_id END),
        COUNT(CASE WHEN ee.event_type = 'unsubscribe' THEN 1 END),
        COUNT(CASE WHEN ee.event_type = 'spam_report' THEN 1 END),
        ROUND(COUNT(CASE WHEN el.status = 'delivered' THEN 1 END)::NUMERIC / 
              NULLIF(COUNT(CASE WHEN el.status IN ('sent', 'delivered', 'bounced') THEN 1 END), 0) * 100, 2),
        ROUND(COUNT(DISTINCT CASE WHEN ee.event_type = 'open' THEN ee.recipient_id END)::NUMERIC / 
              NULLIF(COUNT(CASE WHEN el.status = 'delivered' THEN 1 END), 0) * 100, 2),
        ROUND(COUNT(DISTINCT CASE WHEN ee.event_type = 'click' THEN ee.recipient_id END)::NUMERIC / 
              NULLIF(COUNT(CASE WHEN el.status = 'delivered' THEN 1 END), 0) * 100, 2),
        ROUND(COUNT(CASE WHEN el.status = 'bounced' THEN 1 END)::NUMERIC / 
              NULLIF(COUNT(CASE WHEN el.status IN ('sent', 'delivered', 'bounced') THEN 1 END), 0) * 100, 2),
        ROUND(COUNT(CASE WHEN ee.event_type = 'unsubscribe' THEN 1 END)::NUMERIC / 
              NULLIF(COUNT(CASE WHEN el.status = 'delivered' THEN 1 END), 0) * 100, 2),
        CURRENT_TIMESTAMP
    FROM email_logs el
    LEFT JOIN email_events ee ON el.id = ee.email_log_id
    WHERE el.campaign_id = p_campaign_id
    ON CONFLICT (campaign_id) DO UPDATE SET
        total_recipients = EXCLUDED.total_recipients,
        total_sent = EXCLUDED.total_sent,
        total_delivered = EXCLUDED.total_delivered,
        total_bounced = EXCLUDED.total_bounced,
        total_failed = EXCLUDED.total_failed,
        total_opens = EXCLUDED.total_opens,
        unique_opens = EXCLUDED.unique_opens,
        total_clicks = EXCLUDED.total_clicks,
        unique_clicks = EXCLUDED.unique_clicks,
        total_unsubscribes = EXCLUDED.total_unsubscribes,
        total_spam_reports = EXCLUDED.total_spam_reports,
        delivery_rate = EXCLUDED.delivery_rate,
        open_rate = EXCLUDED.open_rate,
        click_rate = EXCLUDED.click_rate,
        bounce_rate = EXCLUDED.bounce_rate,
        unsubscribe_rate = EXCLUDED.unsubscribe_rate,
        last_updated = EXCLUDED.last_updated;
END;
$$ LANGUAGE plpgsql;

-- Procedure: Add to suppression list
CREATE OR REPLACE FUNCTION add_to_suppression(
    p_email VARCHAR,
    p_reason VARCHAR,
    p_description TEXT DEFAULT NULL
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO suppressions (email, reason, description, suppressed_at)
    VALUES (p_email, p_reason, p_description, CURRENT_TIMESTAMP)
    ON CONFLICT (email) DO UPDATE SET
        reason = EXCLUDED.reason,
        description = EXCLUDED.description,
        suppressed_at = EXCLUDED.suppressed_at;
    
    -- Also update recipient status
    UPDATE recipients
    SET subscribed = false,
        unsubscribed_at = CURRENT_TIMESTAMP
    WHERE email = p_email;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Sample Data (for testing)
-- ============================================

-- Insert sample recipients
INSERT INTO recipients (email, first_name, last_name, language, segment, subscribed) VALUES
('john.doe@example.com', 'John', 'Doe', 'en', 'premium', true),
('jane.smith@example.com', 'Jane', 'Smith', 'en', 'standard', true),
('ivan.petrov@example.ru', 'Ivan', 'Petrov', 'ru', 'premium', true),
('maria.garcia@example.es', 'Maria', 'Garcia', 'es', 'standard', true),
('test@example.com', 'Test', 'User', 'en', 'test', true)
ON CONFLICT (email) DO NOTHING;

-- Insert sample campaign
INSERT INTO campaigns (campaign_id, name, type, status, subject_line, from_email, from_name) VALUES
('camp_001', 'Welcome Campaign', 'welcome', 'draft', 'Welcome to our service!', 'noreply@example.com', 'Example Company')
ON CONFLICT (campaign_id) DO NOTHING;

-- ============================================
-- Maintenance queries
-- ============================================

-- Clean old logs (older than 90 days)
-- Run this periodically
-- DELETE FROM email_logs WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '90 days';
-- DELETE FROM email_events WHERE event_timestamp < CURRENT_TIMESTAMP - INTERVAL '90 days';

-- Vacuum tables for performance
-- VACUUM ANALYZE recipients;
-- VACUUM ANALYZE email_logs;
-- VACUUM ANALYZE email_events;
