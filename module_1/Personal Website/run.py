#!/usr/bin/env python3
"""
Entry point for the Flask personal portfolio application.
This file allows the application to be started with 'python run.py' command.
"""

import logging
from app import app

if __name__ == "__main__":
    # Enable debug logging for easier development
    logging.basicConfig(level=logging.DEBUG)
    
    # Run the Flask application on all interfaces, port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
