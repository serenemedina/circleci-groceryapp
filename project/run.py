"""
Run the Flask application
"""
import os
from app import create_app

# Determine which configuration to use based on environment variable
# Defaults to 'development' if FLASK_ENV is not set
config_name = os.environ.get('FLASK_ENV', 'development')

# Create the Flask app using the selected configuration
app = create_app(config_name)

# Run the Flask app on all interfaces (0.0.0.0) for Docker
# Use PORT environment variable if set, otherwise default to 8080
# Debug mode is enabled
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT') or '8080')
