#!/usr/bin/env python3
"""
Graduate School Data Analysis Web Application

This Flask application analyzes graduate school admission data from grad cafe,
implementing PostgreSQL database operations and presenting analytical insights
through a responsive web interface. Built to examine Spring 2025 admission
trends across multiple universities and programs.

Author: Abdullateef Mumin
"""
import os
import logging
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or "abdullateef-mumin-module3-secret-key"

# Configure PostgreSQL database connection
# Uses environment variable for production, falls back to local config for development
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "postgresql://user:password@localhost:5432/gradcafe_analysis"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database with the Flask app
db.init_app(app)

@app.route('/')
def index():
    """
    Main dashboard displaying comprehensive analysis results
    
    Renders the primary interface showing all seven analytical queries
    with interactive charts and statistical summaries of Spring 2025
    graduate school admission data.
    """
    try:
        from query_data import get_all_analysis_results
        raw_results = get_all_analysis_results()
        
        # Convert PostgreSQL results to match template format exactly
        def create_query_structure(answer, question, query="", explanation=""):
            return {
                'answer': answer,
                'question': question,
                'query': query,
                'explanation': explanation
            }
        
        if isinstance(raw_results, dict):
            # Extract numeric values safely
            def safe_extract_percentage(value):
                if isinstance(value, dict):
                    return float(str(value.get('answer', '0')).replace('%', ''))
                return float(str(value).replace('%', ''))
            
            def safe_extract_number(value):
                if isinstance(value, dict):
                    return value.get('answer', 0)
                return value
            
            results = {
                'spring_2025_count': safe_extract_number(raw_results.get('spring_2025_entries', 0)),
                'international_percentage': safe_extract_percentage(raw_results.get('international_percentage', '0')),
                'average_scores': safe_extract_number(raw_results.get('average_scores', {})),
                'american_spring_2025_gpa': safe_extract_number(raw_results.get('american_spring_2025_gpa', 0)),
                'spring_2025_acceptance_rate': safe_extract_percentage(raw_results.get('spring_2025_acceptance_rate', '0')),
                'accepted_spring_2025_gpa': safe_extract_number(raw_results.get('accepted_spring_2025_gpa', 0)),
                'jhu_cs_masters_count': safe_extract_number(raw_results.get('jhu_cs_masters_count', 0)),
                'detailed_results': {
                    'spring_2025_entries': raw_results.get('spring_2025_entries', {}),
                    'international_percentage': raw_results.get('international_percentage', {}),
                    'average_scores': raw_results.get('average_scores', {}),
                    'american_spring_2025_gpa': raw_results.get('american_spring_2025_gpa', {}),
                    'spring_2025_acceptance_rate': raw_results.get('spring_2025_acceptance_rate', {}),
                    'accepted_spring_2025_gpa': raw_results.get('accepted_spring_2025_gpa', {}),
                    'jhu_cs_masters_count': raw_results.get('jhu_cs_masters_count', {})
                },
                'metadata': {
                    'database_type': 'PostgreSQL',
                    'author': 'Abdullateef Mumin'
                }
            }
        else:
            results = {'error': 'Invalid data format from analysis'}
        
        # Log successful data retrieval
        logger.info(f"Successfully retrieved analysis results with {len(results.get('detailed_results', {}))} queries")
        
        return render_template('index.html', results=results)
    except Exception as e:
        logger.error(f"Error retrieving analysis results: {str(e)}")
        return render_template('index.html', 
                             error=f"Unable to load analysis data: {str(e)}")

@app.route('/api/results')
def api_results():
    """
    JSON API endpoint for programmatic access to analysis results
    
    Returns all query results in JSON format for external applications
    or AJAX requests from the frontend interface.
    """
    try:
        from query_data import get_all_analysis_results
        results = get_all_analysis_results()
        
        logger.info("API request fulfilled successfully")
        return jsonify(results)
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Simple health check endpoint for monitoring"""
    return jsonify({"status": "healthy", "author": "Abdullateef Mumin"})

if __name__ == '__main__':
    # Initialize database and load sample data if needed
    with app.app_context():
        try:
            # Import models to ensure tables are created
            from models import Applicant
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Load sample data if database is empty
            if Applicant.query.count() == 0:
                logger.info("Database is empty, loading initial data...")
                from load_data import main as load_data_main
                load_data_main()
                logger.info("Initial data loaded successfully")
            else:
                logger.info(f"Database contains {Applicant.query.count()} applicant records")
                
        except Exception as e:
            logger.warning(f"Database initialization issue: {e}")
    
    # Start the development server
    logger.info("Starting Flask development server...")
    app.run(host='0.0.0.0', port=5000, debug=True)