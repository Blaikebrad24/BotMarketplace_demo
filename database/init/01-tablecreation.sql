-- ENABLE UUID extension 
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table: users
-- Description: Stores user information.
-- Columns:
--   id: UUID, Primary Key, auto-generated unique identifier.
--   email: VARCHAR(255), unique, not null, user's email address.
--   username: VARCHAR(100), unique, not null, user's username.
--   password_hash: VARCHAR(255), not null, hashed password.
--   first_name: VARCHAR(100), user's first name.
--   last_name: VARCHAR(100), user's last name.
--   is_active: BOOLEAN, default true, indicates if the user is active.
--   is_verified: BOOLEAN, default false, indicates if the user is verified.
--   subscription_tier: VARCHAR(50), default 'free', user's subscription tier.
--   created_at: TIMESTAMP, default current timestamp, record creation time.
--   updated_at: TIMESTAMP, default current timestamp, record update time.
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    subscription_tier VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: categories
-- Description: Stores categories for bots.
-- Columns:
--   id: UUID, Primary Key, auto-generated unique identifier.
--   name: VARCHAR(100), unique, not null, category name.
--   description: TEXT, category description.
--   icon_url: VARCHAR(255), URL for category icon.
--   is_active: BOOLEAN, default true, indicates if the category is active.
--   created_at: TIMESTAMP, default current timestamp, record creation time.
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon_url VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: bots
-- Description: Stores bot information.
-- Columns:
--   id: UUID, Primary Key, auto-generated unique identifier.
--   name: VARCHAR(255), not null, bot name.
--   description: TEXT, brief bot description.
--   detailed_description: TEXT, detailed bot description.
--   price: DECIMAL(10, 2), not null, bot price.
--   is_free: BOOLEAN, default false, indicates if the bot is free.
--   difficulty_level: VARCHAR(50), default 'beginner', bot difficulty level.
--   python_version: VARCHAR(20), default '3.9+', required Python version.
--   execution_time_estimate: INTEGER, estimated execution time in seconds.
--   docker_image: VARCHAR(255), Docker image for the bot.
--   github_repo_url: VARCHAR(255), URL to bot's GitHub repository.
--   demo_video_url: VARCHAR(255), URL to bot's demo video.
--   thumbnail_url: VARCHAR(255), URL to bot's thumbnail image.
--   is_active: BOOLEAN, default true, indicates if the bot is active.
--   download_count: INTEGER, default 0, number of downloads.
--   rating_average: DECIMAL(3, 2), default 0.00, average rating.
--   rating_count: INTEGER, default 0, number of ratings.
--   created_at: TIMESTAMP, default current timestamp, record creation time.
--   updated_at: TIMESTAMP, default current timestamp, record update time.
CREATE TABLE bots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    detailed_description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    is_free BOOLEAN DEFAULT false,
    difficulty_level VARCHAR(50) DEFAULT 'beginner',
    python_version VARCHAR(20) DEFAULT '3.9+',
    execution_time_estimate INTEGER,
    docker_image VARCHAR(255),
    github_repo_url VARCHAR(255),
    demo_video_url VARCHAR(255),
    thumbnail_url VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    download_count INTEGER DEFAULT 0,
    rating_average DECIMAL(3, 2) DEFAULT 0.00,
    rating_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: bot_categories
-- Description: Junction table linking bots and categories.
-- Columns:
--   bot_id: UUID, foreign key referencing bots(id), cascade on delete.
--   category_id: UUID, foreign key referencing categories(id), cascade on delete.
CREATE TABLE bot_categories (
    bot_id UUID REFERENCES bots(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (bot_id, category_id)
);

-- Table: orders
-- Description: Stores user orders.
-- Columns:
--   id: UUID, Primary Key, auto-generated unique identifier.
--   user_id: UUID, foreign key referencing users(id), set null on delete.
--   total_amount: DECIMAL(10, 2), not null, total order amount.
--   stripe_payment_intent_id: VARCHAR(255), Stripe payment intent ID.
--   payment_status: VARCHAR(50), default 'pending', payment status.
--   order_status: VARCHAR(50), default 'processing', order status.
--   created_at: TIMESTAMP, default current timestamp, record creation time.
--   updated_at: TIMESTAMP, default current timestamp, record update time.
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    stripe_payment_intent_id VARCHAR(255),
    payment_status VARCHAR(50) DEFAULT 'pending',
    order_status VARCHAR(50) DEFAULT 'processing',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: order_items
-- Description: Stores items within an order.
-- Columns:
--   id: UUID, Primary Key, auto-generated unique identifier.
--   order_id: UUID, foreign key referencing orders(id), cascade on delete.
--   bot_id: UUID, foreign key referencing bots(id), set null on delete.
--   quantity: INTEGER, default 1, quantity of the bot purchased.
--   price_at_purchase: DECIMAL(10, 2), not null, price at purchase time.
--   created_at: TIMESTAMP, default current timestamp, record creation time.
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    bot_id UUID REFERENCES bots(id) ON DELETE SET NULL,
    quantity INTEGER DEFAULT 1,
    price_at_purchase DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: bot_executions
-- Description: Stores bot execution details.
-- Columns:
--   id: UUID, Primary Key, auto-generated unique identifier.
--   user_id: UUID, foreign key referencing users(id), set null on delete.
--   bot_id: UUID, foreign key referencing bots(id), set null on delete.
--   execution_status: VARCHAR(50), default 'queued', execution status.
--   input_parameters: JSONB, input parameters for execution.
--   output_data: JSONB, output data from execution.
--   execution_time: INTEGER, execution time in seconds.
--   error_message: TEXT, error message if execution fails.
--   container_id: VARCHAR(255), container ID for execution.
--   started_at: TIMESTAMP, execution start time.
--   completed_at: TIMESTAMP, execution completion time.
--   created_at: TIMESTAMP, default current timestamp, record creation time.
CREATE TABLE bot_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    bot_id UUID REFERENCES bots(id) ON DELETE SET NULL,
    execution_status VARCHAR(50) DEFAULT 'queued',
    input_parameters JSONB,
    output_data JSONB,
    execution_time INTEGER,
    error_message TEXT,
    container_id VARCHAR(255),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: execution_logs
-- Description: Stores logs for bot executions.
-- Columns:
--   id: UUID, Primary Key, auto-generated unique identifier.
--   execution_id: UUID, foreign key referencing bot_executions(id), cascade on delete.
--   log_level: VARCHAR(20), default 'INFO', log level.
--   message: TEXT, not null, log message.
--   timestamp: TIMESTAMP, default current timestamp, log timestamp.
--   created_at: TIMESTAMP, default current timestamp, record creation time.
CREATE TABLE execution_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_id UUID REFERENCES bot_executions(id) ON DELETE CASCADE,
    log_level VARCHAR(20) DEFAULT 'INFO',
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: bot_reviews
-- Description: Stores user reviews for bots.
-- Columns:
--   id: UUID, Primary Key, auto-generated unique identifier.
--   user_id: UUID, foreign key referencing users(id), set null on delete.
--   bot_id: UUID, foreign key referencing bots(id), cascade on delete.
--   rating: INTEGER, rating between 1 and 5.
--   review_text: TEXT, review text.
--   is_verified_purchase: BOOLEAN, default false, indicates if the review is from a verified purchase.
--   created_at: TIMESTAMP, default current timestamp, record creation time.
--   updated_at: TIMESTAMP, default current timestamp, record update time.
--   UNIQUE(user_id, bot_id): Ensures a user can only review a bot once.
CREATE TABLE bot_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    bot_id UUID REFERENCES bots(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    is_verified_purchase BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, bot_id)
);

-- Table: user_bot_access
-- Description: Stores user access permissions for bots.
-- Columns:
--   id: UUID, Primary Key, auto-generated unique identifier.
--   user_id: UUID, foreign key referencing users(id), cascade on delete.
--   bot_id: UUID, foreign key referencing bots(id), cascade on delete.
--   access_type: VARCHAR(50), default 'purchased', type of access.
--   granted_at: TIMESTAMP, default current timestamp, access grant time.
--   expires_at: TIMESTAMP, access expiration time.
--   is_active: BOOLEAN, default true, indicates if access is active.
--   UNIQUE(user_id, bot_id): Ensures a user can only have one access record per bot.
CREATE TABLE user_bot_access (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    bot_id UUID REFERENCES bots(id) ON DELETE CASCADE,
    access_type VARCHAR(50) DEFAULT 'purchased',
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    UNIQUE(user_id, bot_id)
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_bots_name ON bots(name);
CREATE INDEX idx_bots_price ON bots(price);
CREATE INDEX idx_bots_rating ON bots(rating_average);
CREATE INDEX idx_bots_active ON bots(is_active);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_executions_user_id ON bot_executions(user_id);
CREATE INDEX idx_executions_bot_id ON bot_executions(bot_id);
CREATE INDEX idx_executions_status ON bot_executions(execution_status);
CREATE INDEX idx_executions_created_at ON bot_executions(created_at);
CREATE INDEX idx_user_bot_access_user_id ON user_bot_access(user_id);
CREATE INDEX idx_user_bot_access_bot_id ON user_bot_access(bot_id);