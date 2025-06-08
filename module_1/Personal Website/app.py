"""
Main Flask application factory and configuration.
Sets up the Flask app with blueprints and necessary configurations.
"""

import os
from flask import Flask

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Set secret key for session management
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    
    # Register blueprints for modular page organization
    from blueprints.main import main_bp
    from blueprints.contact import contact_bp
    from blueprints.projects import projects_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(projects_bp)
    
    return app

# Create the app instance
app = create_app()
