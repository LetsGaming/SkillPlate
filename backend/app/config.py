import os
from datetime import timedelta

class Config:
    """
    Base configuration. 
    Values here are used across all environments unless overridden.
    """
    # General Flask Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-12345")
    DEBUG = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")
    PORT = int(os.getenv("PORT", 5000))

    # JWT Settings
    # In production, this MUST be a strong, random secret
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-super-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Database Settings (Placeholder for when you add SQLAlchemy)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # In production, we should force the use of environment variables
    # If they are missing, the app will fail to start (which is good)
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

# Dictionary to help select the config based on an environment variable
config_by_name = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}