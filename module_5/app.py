#!/usr/bin/env python3
"""
Graduate School Data Analysis Web Application - PostgreSQL Version.

This application provides comprehensive analysis of graduate school admission
data using secure SQL queries and Flask web framework.

Author: Abdullateef Mumin
"""

import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base class."""


# Create database instance
db = SQLAlchemy(model_class=Base)

# Create Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize database
db.init_app(app)

# Import models to ensure tables are created
import models  # pylint: disable=import-outside-toplevel,unused-import

# Import routes after app initialization
from routes import *  # pylint: disable=import-outside-toplevel,wildcard-import,unused-wildcard-import

logger.info("Flask application initialized successfully")
