"""
Pytest fixtures for the Grocery Flask application
"""

import pytest
from project.app import create_app, db

# Create and yield a Flask app instance configured for testing
@pytest.fixture
def app():
    app = create_app(config_name='testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

# Create and return a test client for the Flask app
@pytest.fixture
def client(app):
    return app.test_client()