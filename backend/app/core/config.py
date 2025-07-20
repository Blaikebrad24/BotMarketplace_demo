
from typing import List, Optional 
from pydantic_settings import BaseSettings
from pydantic import Field 
import os 
from dotenv import load_dotenv 

class Settings(BaseSettings):
    
    """
        Application settings for the Bot Marketplace API.

        This class defines the configuration settings for the application using Pydantic.
        It includes settings for API endpoints, database connection, security, CORS, 
        environment variables, Redis, and external API keys. Pydantic will validate 
        required fields and ensure that the application is configured correctly.

        Attributes:
            API_V1_STR (str): The versioned API endpoint.
            PROJECT_NAME (str): The name of the project.
            VERSION (str): The current version of the application.
            DESCRIPTION (str): A brief description of the API.
            DATABASE_URL (str): The database connection URL.
            DB_POOL_SIZE (int): The size of the database connection pool.
            DB_MAX_OVERFLOW (int): The maximum overflow size for the database connection pool.
            SECRET_KEY (str): The secret key for security purposes.
            ALGORITHM (str): The algorithm used for token encoding.
            ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for access tokens in minutes.
            ALLOWED_HOSTS (List[str]): A list of allowed hosts for CORS.
            ENVIRONMENT (str): The current environment (e.g., development, production).
            DEBUG (bool): A flag indicating whether debugging is enabled.
            REDIS_URL (str): The Redis connection URL.
            STRIPE_SECRET_KEY (Optional[str]): The secret key for Stripe API.
            OPENAI_API_KEY (Optional[str]): The API key for OpenAI services.
    """
    
    load_dotenv()
    # API Settings 
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME : str = "1.0.0"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for the Bot Marketplace application"
    
    # Database settings 
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # Database connection pool settings
    DB_POOL_SIZE: int = Field(default=5, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(default=10, env="DB_MAX_OVERFLOW")
    
    # Security Settings 
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS Settings (Cross-Origin Resource Sharing)
    ALLOWED_HOSTS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"], 
        env="ALLOWED_HOSTS"
    )
    
    # Environment
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Redis Settings
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # External API Keys
    STRIPE_SECRET_KEY: Optional[str] = Field(default=None, env="STRIPE_SECRET_KEY")
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    
    class Config:
        # This tells Pydantic to load values from .env file
        env_file = ".env"
        case_sensitive = True

settings = Settings()
    