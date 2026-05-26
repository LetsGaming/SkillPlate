import os
from datetime import timedelta

class Config:
    """
    Base configuration. 
    Values here are used across all environments unless overridden.
    """
    VERSION_PATH = "/v1"

    # General Flask Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-12345")
    DEBUG = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")
    PORT = int(os.getenv("PORT", 5000))

    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

    # Required for HttpOnly refresh token cookie
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SECURE = os.getenv("FLASK_ENV", "development") == "production"  # HTTPS only in prod
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_CSRF_PROTECT = False  # Set True in production with proper CSRF handling

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