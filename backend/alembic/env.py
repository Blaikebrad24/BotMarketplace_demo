from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.db.session.database import Base

# Import all models to ensure they're registered with SQLAlchemy
from app.models.UserModel import UserModel
from app.models.CategoryModel import CategoryModel
from app.models.BotModel import BotModel
from app.models.Associations import bot_categories
from app.models.Bot_executionModel import BotExecutionModel
from app.models.Bot_ReviewModel import BotReviewModel
from app.models.ExecutionLogModel import ExecutionLogModel
from app.models.OrderModel import OrderModel
from app.models.OrderItemModel import OrderItemModel
from app.models.User_Bot_AccessModel import UserBotAccessModel


# this is the Alembic Config object
config = context.config

# Set the database URL from our settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the MetaData object for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    This is used when you want to generate SQL scripts without connecting to the database.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    This connects to the database and applies migrations.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()