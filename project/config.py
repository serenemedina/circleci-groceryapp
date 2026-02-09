"""
Application configuration module for multiple Flask environments.
Defines base, development, testing, and production settings.
"""
import os

# Base configuration with defaults shared across all environments
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    # Disable SQLAlchemy event notifications for performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    @staticmethod
    def init_app(app):
        pass

# Development environment configuration
class DevelopmentConfig(Config):
    DEBUG = True
    # Use local PostgreSQL by default if DATABASE_URL is not set
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:password@localhost:5432/dev_db' 

# Testing environment configuration
class TestingConfig(Config):
    TESTING = True
    DEBUG = True 
    # Use a separate test database
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'postgresql://postgres:password@localhost:5432/test_db' 

# Production environment configuration
class ProductionConfig(Config):
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # Must be set via environment variable in production

# Map environment names to configuration classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}