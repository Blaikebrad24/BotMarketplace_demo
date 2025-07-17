-- Insert sample categories
INSERT INTO categories (name, description, icon_url) VALUES
('Productivity', 'Bots that help with daily productivity tasks', '/icons/productivity.svg'),
('File Management', 'Bots for organizing and managing files', '/icons/files.svg'),
('Web Scraping', 'Bots for extracting data from websites', '/icons/web.svg'),
('AI & Machine Learning', 'Bots powered by AI and ML algorithms', '/icons/ai.svg'),
('Email & Communication', 'Bots for email and messaging automation', '/icons/email.svg'),
('Data Processing', 'Bots for data analysis and processing', '/icons/data.svg');

-- Insert sample bots
INSERT INTO bots (name, description, detailed_description, price, difficulty_level, python_version, execution_time_estimate, thumbnail_url) VALUES
('File Organizer Pro', 'Automatically organize files by type, date, and custom rules', 'A powerful file organization bot that can sort your downloads, documents, and media files automatically. Features include duplicate detection, custom naming conventions, and scheduled organization.', 9.99, 'beginner', '3.9+', 30, '/thumbnails/file-organizer.jpg'),
('Email Newsletter Bot', 'Automate email newsletter creation and sending', 'Create and send beautiful email newsletters automatically. Supports template customization, subscriber management, and analytics tracking.', 19.99, 'intermediate', '3.10+', 120, '/thumbnails/email-bot.jpg'),
('Web Data Scraper', 'Extract data from websites with custom rules', 'Advanced web scraping bot with support for JavaScript rendering, API integration, and data export to multiple formats.', 29.99, 'advanced', '3.11+', 300, '/thumbnails/web-scraper.jpg'),
('AI Content Generator', 'Generate content using OpenAI GPT models', 'Create blog posts, social media content, and marketing copy using advanced AI models. Includes content optimization and SEO features.', 39.99, 'intermediate', '3.11+', 60, '/thumbnails/ai-content.jpg'),
('Free File Cleaner', 'Clean up duplicate and unnecessary files', 'A free bot to help you clean up your computer by finding and removing duplicate files, empty folders, and temporary files.', 0.00, 'beginner', '3.9+', 45, '/thumbnails/file-cleaner.jpg');

-- Link bots to categories
INSERT INTO bot_categories (bot_id, category_id) 
SELECT b.id, c.id FROM bots b, categories c 
WHERE (b.name = 'File Organizer Pro' AND c.name = 'File Management')
   OR (b.name = 'File Organizer Pro' AND c.name = 'Productivity')
   OR (b.name = 'Email Newsletter Bot' AND c.name = 'Email & Communication')
   OR (b.name = 'Email Newsletter Bot' AND c.name = 'Productivity')
   OR (b.name = 'Web Data Scraper' AND c.name = 'Web Scraping')
   OR (b.name = 'Web Data Scraper' AND c.name = 'Data Processing')
   OR (b.name = 'AI Content Generator' AND c.name = 'AI & Machine Learning')
   OR (b.name = 'AI Content Generator' AND c.name = 'Productivity')
   OR (b.name = 'Free File Cleaner' AND c.name = 'File Management')
   OR (b.name = 'Free File Cleaner' AND c.name = 'Productivity');

-- Create a test user (password is 'testpassword123' hashed with bcrypt)
INSERT INTO users (email, username, password_hash, first_name, last_name, is_verified) VALUES
('test@example.com', 'testuser', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBzBR5QgjUmGAS', 'Test', 'User', true);