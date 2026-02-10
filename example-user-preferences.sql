-- ============================================
-- Example User Preferences Data
-- For Customer Acquisition Email Campaign
-- ============================================

-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    status VARCHAR(50) DEFAULT 'lead',
    email_verified BOOLEAN DEFAULT false,
    unsubscribed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    last_activity_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    interests TEXT, -- comma-separated: automation,analytics,integration,security
    preferred_language VARCHAR(10) DEFAULT 'en',
    industry VARCHAR(100), -- technology, finance, healthcare, retail, other
    company_size VARCHAR(50), -- small, medium, large, enterprise
    job_role VARCHAR(100), -- developer, manager, executive, etc.
    communication_frequency VARCHAR(50), -- daily, weekly, monthly
    opt_in_marketing BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS email_campaigns (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    campaign_name VARCHAR(255),
    email_subject TEXT,
    template_id VARCHAR(100),
    segment VARCHAR(100),
    sent_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50), -- sent, failed, bounced
    opened_at TIMESTAMP,
    clicked_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS email_errors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    campaign_name VARCHAR(255),
    error_message TEXT,
    error_date TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
CREATE INDEX IF NOT EXISTS idx_users_email_verified ON users(email_verified);
CREATE INDEX IF NOT EXISTS idx_user_preferences_industry ON user_preferences(industry);
CREATE INDEX IF NOT EXISTS idx_user_preferences_opt_in ON user_preferences(opt_in_marketing);
CREATE INDEX IF NOT EXISTS idx_email_campaigns_sent_at ON email_campaigns(sent_at);
CREATE INDEX IF NOT EXISTS idx_email_campaigns_user_id ON email_campaigns(user_id);

-- ============================================
-- Insert Example Users - Technology Industry
-- ============================================

INSERT INTO users (email, first_name, last_name, status, email_verified, unsubscribed, created_at, last_activity_date)
VALUES 
    ('john.smith@techcorp.com', 'John', 'Smith', 'lead', true, false, NOW() - INTERVAL '5 days', NOW() - INTERVAL '1 day'),
    ('sarah.johnson@devstudio.io', 'Sarah', 'Johnson', 'lead', true, false, NOW() - INTERVAL '10 days', NOW() - INTERVAL '2 days'),
    ('mike.chen@cloudtech.com', 'Mike', 'Chen', 'lead', true, false, NOW() - INTERVAL '3 days', NOW() - INTERVAL '1 day')
ON CONFLICT (email) DO NOTHING;

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'automation,integration,analytics',
    'en',
    'technology',
    'medium',
    'CTO',
    'weekly',
    true
FROM users u WHERE u.email = 'john.smith@techcorp.com'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    updated_at = NOW();

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'automation,security',
    'en',
    'technology',
    'small',
    'Lead Developer',
    'weekly',
    true
FROM users u WHERE u.email = 'sarah.johnson@devstudio.io'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    updated_at = NOW();

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'integration,analytics,security',
    'en',
    'technology',
    'large',
    'Engineering Manager',
    'monthly',
    true
FROM users u WHERE u.email = 'mike.chen@cloudtech.com'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    updated_at = NOW();

-- ============================================
-- Insert Example Users - Finance Industry
-- ============================================

INSERT INTO users (email, first_name, last_name, status, email_verified, unsubscribed, created_at, last_activity_date)
VALUES 
    ('emily.davis@financegroup.com', 'Emily', 'Davis', 'lead', true, false, NOW() - INTERVAL '7 days', NOW() - INTERVAL '1 day'),
    ('robert.wilson@banktech.com', 'Robert', 'Wilson', 'lead', true, false, NOW() - INTERVAL '4 days', NOW() - INTERVAL '2 days')
ON CONFLICT (email) DO NOTHING;

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'security,analytics,automation',
    'en',
    'finance',
    'enterprise',
    'Chief Risk Officer',
    'monthly',
    true
FROM users u WHERE u.email = 'emily.davis@financegroup.com'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    updated_at = NOW();

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'security,integration',
    'en',
    'finance',
    'large',
    'IT Director',
    'weekly',
    true
FROM users u WHERE u.email = 'robert.wilson@banktech.com'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    updated_at = NOW();

-- ============================================
-- Insert Example Users - Healthcare Industry
-- ============================================

INSERT INTO users (email, first_name, last_name, status, email_verified, unsubscribed, created_at, last_activity_date)
VALUES 
    ('dr.lisa.martinez@healthsys.org', 'Lisa', 'Martinez', 'lead', true, false, NOW() - INTERVAL '6 days', NOW() - INTERVAL '1 day'),
    ('james.brown@medtech.com', 'James', 'Brown', 'lead', true, false, NOW() - INTERVAL '8 days', NOW() - INTERVAL '3 days')
ON CONFLICT (email) DO NOTHING;

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'security,analytics',
    'en',
    'healthcare',
    'large',
    'Chief Medical Information Officer',
    'monthly',
    true
FROM users u WHERE u.email = 'dr.lisa.martinez@healthsys.org'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    updated_at = NOW();

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'integration,automation,security',
    'en',
    'healthcare',
    'medium',
    'Healthcare IT Manager',
    'weekly',
    true
FROM users u WHERE u.email = 'james.brown@medtech.com'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    updated_at = NOW();

-- ============================================
-- Insert Example Users - Retail Industry
-- ============================================

INSERT INTO users (email, first_name, last_name, status, email_verified, unsubscribed, created_at, last_activity_date)
VALUES 
    ('anna.taylor@retailchain.com', 'Anna', 'Taylor', 'lead', true, false, NOW() - INTERVAL '2 days', NOW() - INTERVAL '1 day'),
    ('david.lee@ecommerce.shop', 'David', 'Lee', 'lead', true, false, NOW() - INTERVAL '9 days', NOW() - INTERVAL '2 days')
ON CONFLICT (email) DO NOTHING;

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'analytics,automation',
    'en',
    'retail',
    'large',
    'Director of Operations',
    'weekly',
    true
FROM users u WHERE u.email = 'anna.taylor@retailchain.com'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    updated_at = NOW();

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'integration,analytics,automation',
    'en',
    'retail',
    'medium',
    'E-commerce Manager',
    'weekly',
    true
FROM users u WHERE u.email = 'david.lee@ecommerce.shop'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    updated_at = NOW();

-- ============================================
-- Insert Example Users - Other Industries
-- ============================================

INSERT INTO users (email, first_name, last_name, status, email_verified, unsubscribed, created_at, last_activity_date)
VALUES 
    ('maria.garcia@consulting.pro', 'Maria', 'Garcia', 'lead', true, false, NOW() - INTERVAL '12 days', NOW() - INTERVAL '4 days'),
    ('thomas.anderson@manufacturing.com', 'Thomas', 'Anderson', 'lead', true, false, NOW() - INTERVAL '5 days', NOW() - INTERVAL '1 day')
ON CONFLICT (email) DO NOTHING;

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'automation,analytics',
    'en',
    'consulting',
    'small',
    'Managing Partner',
    'monthly',
    true
FROM users u WHERE u.email = 'maria.garcia@consulting.pro'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    updated_at = NOW();

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'automation,integration',
    'en',
    'manufacturing',
    'enterprise',
    'VP of Operations',
    'weekly',
    true
FROM users u WHERE u.email = 'thomas.anderson@manufacturing.com'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    updated_at = NOW();

-- ============================================
-- Insert Example Users - Multilingual
-- ============================================

INSERT INTO users (email, first_name, last_name, status, email_verified, unsubscribed, created_at, last_activity_date)
VALUES 
    ('pierre.dubois@entreprise.fr', 'Pierre', 'Dubois', 'lead', true, false, NOW() - INTERVAL '6 days', NOW() - INTERVAL '2 days'),
    ('hans.mueller@firma.de', 'Hans', 'Mueller', 'lead', true, false, NOW() - INTERVAL '7 days', NOW() - INTERVAL '1 day')
ON CONFLICT (email) DO NOTHING;

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'automation,security',
    'fr',
    'technology',
    'medium',
    'Directeur Technique',
    'weekly',
    true
FROM users u WHERE u.email = 'pierre.dubois@entreprise.fr'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    preferred_language = EXCLUDED.preferred_language,
    updated_at = NOW();

INSERT INTO user_preferences (user_id, interests, preferred_language, industry, company_size, job_role, communication_frequency, opt_in_marketing)
SELECT 
    u.id,
    'integration,analytics',
    'de',
    'finance',
    'large',
    'IT-Leiter',
    'monthly',
    true
FROM users u WHERE u.email = 'hans.mueller@firma.de'
ON CONFLICT (user_id) DO UPDATE SET
    interests = EXCLUDED.interests,
    industry = EXCLUDED.industry,
    preferred_language = EXCLUDED.preferred_language,
    updated_at = NOW();

-- ============================================
-- Verification Queries
-- ============================================

-- Check total leads with preferences
SELECT 
    COUNT(*) as total_leads,
    COUNT(CASE WHEN up.opt_in_marketing = true THEN 1 END) as opted_in
FROM users u
LEFT JOIN user_preferences up ON u.id = up.user_id
WHERE u.status = 'lead' AND u.email_verified = true;

-- Check distribution by industry
SELECT 
    up.industry,
    COUNT(*) as count,
    STRING_AGG(DISTINCT up.interests, '; ') as common_interests
FROM users u
JOIN user_preferences up ON u.id = up.user_id
WHERE u.status = 'lead' 
    AND u.email_verified = true 
    AND up.opt_in_marketing = true
GROUP BY up.industry
ORDER BY count DESC;

-- Check distribution by interests
SELECT 
    interest,
    COUNT(*) as count
FROM (
    SELECT 
        u.id,
        TRIM(unnest(string_to_array(up.interests, ','))) as interest
    FROM users u
    JOIN user_preferences up ON u.id = up.user_id
    WHERE u.status = 'lead' 
        AND u.email_verified = true 
        AND up.opt_in_marketing = true
) subquery
GROUP BY interest
ORDER BY count DESC;

-- Check distribution by company size
SELECT 
    up.company_size,
    COUNT(*) as count
FROM users u
JOIN user_preferences up ON u.id = up.user_id
WHERE u.status = 'lead' 
    AND u.email_verified = true 
    AND up.opt_in_marketing = true
GROUP BY up.company_size
ORDER BY count DESC;

-- ============================================
-- Sample Query for Workflow Testing
-- ============================================

-- This query matches the one used in the n8n workflow
SELECT 
    u.id,
    u.email,
    u.first_name,
    u.last_name,
    up.interests,
    up.preferred_language,
    up.industry,
    up.company_size,
    up.job_role,
    up.communication_frequency,
    u.created_at,
    u.last_activity_date
FROM users u
LEFT JOIN user_preferences up ON u.id = up.user_id
WHERE u.status = 'lead'
    AND u.email_verified = true
    AND (u.unsubscribed = false OR u.unsubscribed IS NULL)
    AND up.opt_in_marketing = true
ORDER BY u.created_at DESC
LIMIT 10;
