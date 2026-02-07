-- Database schema for VK Content Workflow logging
-- Supports PostgreSQL, MySQL, and SQLite with minor modifications

-- Table for storing post logs
CREATE TABLE IF NOT EXISTS vk_posts_log (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(255),
    owner_id VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    attachments TEXT,
    topic VARCHAR(255),
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_owner_id (owner_id)
);

-- Table for storing post statistics
CREATE TABLE IF NOT EXISTS vk_posts_stats (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(255) NOT NULL,
    owner_id VARCHAR(255) NOT NULL,
    views_count INT DEFAULT 0,
    likes_count INT DEFAULT 0,
    reposts_count INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES vk_posts_log(post_id) ON DELETE CASCADE,
    INDEX idx_post_id (post_id),
    INDEX idx_collected_at (collected_at)
);

-- Table for storing workflow execution logs
CREATE TABLE IF NOT EXISTS workflow_executions (
    id SERIAL PRIMARY KEY,
    execution_id VARCHAR(255) UNIQUE NOT NULL,
    workflow_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP,
    duration_ms INT,
    error_message TEXT,
    INDEX idx_execution_id (execution_id),
    INDEX idx_status (status),
    INDEX idx_started_at (started_at)
);

-- Table for storing content templates
CREATE TABLE IF NOT EXISTS content_templates (
    id SERIAL PRIMARY KEY,
    template_name VARCHAR(255) NOT NULL,
    template_text TEXT NOT NULL,
    topic VARCHAR(255),
    hashtags TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    usage_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_topic (topic),
    INDEX idx_is_active (is_active)
);

-- Table for storing VK API rate limits
CREATE TABLE IF NOT EXISTS vk_rate_limits (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    requests_count INT DEFAULT 0,
    window_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    window_end TIMESTAMP,
    INDEX idx_endpoint (endpoint),
    INDEX idx_window_start (window_start)
);

-- View for post analytics
CREATE OR REPLACE VIEW vk_posts_analytics AS
SELECT 
    l.id,
    l.post_id,
    l.owner_id,
    l.topic,
    l.status,
    l.created_at,
    s.views_count,
    s.likes_count,
    s.reposts_count,
    s.comments_count,
    (s.likes_count + s.reposts_count * 2 + s.comments_count * 3) AS engagement_score
FROM 
    vk_posts_log l
LEFT JOIN 
    vk_posts_stats s ON l.post_id = s.post_id
WHERE 
    l.status = 'success'
ORDER BY 
    l.created_at DESC;

-- View for workflow performance
CREATE OR REPLACE VIEW workflow_performance AS
SELECT 
    workflow_name,
    COUNT(*) AS total_executions,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) AS successful_executions,
    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed_executions,
    AVG(duration_ms) AS avg_duration_ms,
    MIN(duration_ms) AS min_duration_ms,
    MAX(duration_ms) AS max_duration_ms,
    DATE(started_at) AS execution_date
FROM 
    workflow_executions
GROUP BY 
    workflow_name, DATE(started_at)
ORDER BY 
    execution_date DESC;

-- Function to update timestamp on row update
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for vk_posts_log
CREATE TRIGGER update_vk_posts_log_updated_at
BEFORE UPDATE ON vk_posts_log
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for content_templates
CREATE TRIGGER update_content_templates_updated_at
BEFORE UPDATE ON content_templates
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Insert sample content templates
INSERT INTO content_templates (template_name, template_text, topic, hashtags) VALUES
('Motivation 1', '🚀 Новый день - новые возможности! Используйте каждую минуту с пользой!', 'мотивация', '#мотивация #успех #развитие'),
('Motivation 2', '💪 Верьте в себя и свои силы. Вы способны на большее, чем думаете!', 'мотивация', '#мотивация #вера #сила'),
('Productivity 1', '⏰ Планируйте день с вечера - и утро станет продуктивнее в разы!', 'продуктивность', '#продуктивность #планирование #эффективность'),
('Productivity 2', '📊 Фокусируйтесь на главном, а не на срочном. Расставьте приоритеты!', 'продуктивность', '#продуктивность #приоритеты #фокус'),
('Health 1', '🏃‍♂️ 10 минут зарядки каждое утро = заряд энергии на весь день!', 'здоровье', '#зож #здоровье #спорт'),
('Health 2', '🥗 Правильное питание - это инвестиция в ваше здоровье и энергию!', 'здоровье', '#зож #правильноепитание #здоровье'),
('Career 1', '🎯 Инвестируйте в свои навыки - это лучшая инвестиция в будущее!', 'карьера', '#карьера #развитие #обучение'),
('Career 2', '💼 Успешная карьера строится на постоянном обучении и адаптации!', 'карьера', '#карьера #профессионализм #рост');

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_posts_status_date ON vk_posts_log(status, created_at);
CREATE INDEX IF NOT EXISTS idx_stats_post_collected ON vk_posts_stats(post_id, collected_at);
CREATE INDEX IF NOT EXISTS idx_templates_active_topic ON content_templates(is_active, topic);

-- Comments for documentation
COMMENT ON TABLE vk_posts_log IS 'Stores all VK posts created by the workflow';
COMMENT ON TABLE vk_posts_stats IS 'Stores statistics for published VK posts';
COMMENT ON TABLE workflow_executions IS 'Stores workflow execution logs';
COMMENT ON TABLE content_templates IS 'Stores reusable content templates';
COMMENT ON TABLE vk_rate_limits IS 'Tracks VK API rate limits';

COMMENT ON COLUMN vk_posts_log.status IS 'Status: pending, success, failed, validation_failed';
COMMENT ON COLUMN vk_posts_stats.views_count IS 'Number of post views';
COMMENT ON COLUMN vk_posts_stats.likes_count IS 'Number of likes';
COMMENT ON COLUMN vk_posts_stats.reposts_count IS 'Number of reposts/shares';
COMMENT ON COLUMN vk_posts_stats.comments_count IS 'Number of comments';
