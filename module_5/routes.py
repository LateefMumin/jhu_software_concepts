#!/usr/bin/env python3
"""
Flask routes for the Graduate School Data Analysis application.

Author: Abdullateef Mumin
"""

import logging
from flask import render_template, jsonify
from app import app, db
from query_data import get_all_analysis_results

logger = logging.getLogger(__name__)

# Initialize database tables and load sample data
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")

        # Load sample data if database has insufficient records
        from models import Applicant
        current_count = Applicant.query.count()
        if current_count < 10000:
            logger.info("Loading 10,000 sample records...")
            from load_data import load_sample_data
            load_sample_data()
            logger.info("Sample data loaded successfully")
        else:
            logger.info("Database already contains %s records", current_count)

    except Exception as exc:
        logger.error("Error initializing database: %s", exc)


@app.route('/')
def index():
    """Main dashboard route."""
    try:
        results = get_all_analysis_results()
        return render_template('index.html', results=results)
    except Exception as exc:
        logger.error("Dashboard error: %s", exc)
        return render_template('index.html', error=str(exc))


@app.route('/api/results')
def api_results():
    """JSON API endpoint."""
    try:
        results = get_all_analysis_results()
        return jsonify(results)
    except Exception as exc:
        logger.error("API error: %s", exc)
        return jsonify({'error': str(exc)}), 500


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'database': 'PostgreSQL',
        'security_features': ['SQL injection protection', 'Input validation', 'Query limits'],
        'author': 'Abdullateef Mumin'
    })
