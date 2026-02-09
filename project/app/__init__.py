"""
This module initializes the Flask app and SQLAlchemy database.

Creates and configures the Flask app by:
- Loading environment-specific configuration
- Initializing extensions (SQLAlchemy)
- Registering blueprints
- Creating database tables if they do not exist
"""
from flask import Flask
from .models import db
from config import config

# Create and configure the Flask app with the given environment config (application factory function)
def create_app(config_name):
    app = Flask(__name__)
    
    # Load configuration class based on the environment
    app_config = config[config_name]()
    app.config.from_object(app_config)
    app_config.init_app(app)

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Create database tables only if they don't exist
    with app.app_context():
        db.create_all()
        print()

    # Register the blueprint that contains all the routes
    from .routes import main as main_bp 
    app.register_blueprint(main_bp)

    return app
