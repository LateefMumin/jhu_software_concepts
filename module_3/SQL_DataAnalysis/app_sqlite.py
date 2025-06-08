#!/usr/bin/env python3
"""
Graduate School Data Analysis Web Application - SQLite Version

This SQLite version provides a local development alternative to the PostgreSQL
implementation, using the same analytical queries and web interface but with
a pre-loaded SQLite database for immediate testing and demonstration.

Author: Abdullateef Mumin

This version is provided as a backup for environments where PostgreSQL
setup may be challenging, ensuring the application can be evaluated regardless
of database configuration requirements.
"""
import os
import sqlite3
import logging
from flask import Flask, render_template, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask application for SQLite version
app = Flask(__name__)
app.secret_key = "abdullateef-mumin-sqlite-version-secret"

# SQLite database path
SQLITE_DB_PATH = 'gradcafe.db'

def get_database_connection():
    """Get SQLite database connection with proper configuration"""
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

def execute_query(query, params=None):
    """Execute SQL query with error handling"""
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            result = cursor.rowcount
            conn.commit()
            
        conn.close()
        return result
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        raise

def get_spring_2025_entries():
    """Query 1: Spring 2025 application count"""
    query = "SELECT COUNT(*) as count FROM applicants WHERE term = 'Spring 2025'"
    result = execute_query(query)
    
    return {
        'question': 'How many entries do you have in your database who have applied for Spring 2025?',
        'answer': result[0][0] if result else 0,
        'query': query,
        'explanation': 'Counts all Spring 2025 applications in the database'
    }

def get_international_percentage():
    """Query 2: International student percentage"""
    query = """
    SELECT 
        COUNT(CASE WHEN us_or_international = 'International' THEN 1 END) * 100.0 / COUNT(*) as percentage
    FROM applicants
    """
    result = execute_query(query)
    
    return {
        'question': 'What percentage of entries are from international students?',
        'answer': round(result[0][0], 2) if result and result[0][0] else 0,
        'query': query.strip(),
        'explanation': 'Calculates percentage of international vs domestic students'
    }

def get_average_scores():
    """Query 3: Average academic metrics"""
    query = """
    SELECT 
        AVG(gpa) as avg_gpa,
        AVG(gre) as avg_gre,
        AVG(gre_v) as avg_gre_v,
        AVG(gre_aw) as avg_gre_aw
    FROM applicants
    WHERE gpa IS NOT NULL AND gre IS NOT NULL AND gre_v IS NOT NULL AND gre_aw IS NOT NULL
    """
    result = execute_query(query)
    
    if result and result[0][0]:
        return {
            'question': 'What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?',
            'answer': {
                'avg_gpa': round(result[0][0], 3),
                'avg_gre': round(result[0][1], 1),
                'avg_gre_v': round(result[0][2], 1),
                'avg_gre_aw': round(result[0][3], 2)
            },
            'query': query.strip(),
            'explanation': 'Average scores for applicants with complete academic data'
        }
    return {'question': 'What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?', 'answer': {}}

def get_american_spring_2025_gpa():
    """Query 4: American students Spring 2025 GPA"""
    query = """
    SELECT AVG(gpa) as avg_gpa
    FROM applicants 
    WHERE us_or_international = 'American' AND term = 'Spring 2025' AND gpa IS NOT NULL
    """
    result = execute_query(query)
    
    return {
        'question': 'What is the average GPA of American students in Spring 2025?',
        'answer': round(result[0][0], 3) if result and result[0][0] else 0,
        'query': query.strip(),
        'explanation': 'Average GPA for domestic Spring 2025 applicants'
    }

def get_spring_2025_acceptance_rate():
    """Query 5: Spring 2025 acceptance rate"""
    query = """
    SELECT 
        COUNT(CASE WHEN status = 'Accepted' THEN 1 END) * 100.0 / COUNT(*) as acceptance_rate
    FROM applicants 
    WHERE term = 'Spring 2025'
    """
    result = execute_query(query)
    
    return {
        'question': 'What percent of entries for Spring 2025 are Acceptances?',
        'answer': round(result[0][0], 2) if result and result[0][0] else 0,
        'query': query.strip(),
        'explanation': 'Acceptance rate for Spring 2025 applications'
    }

def get_accepted_spring_2025_gpa():
    """Query 6: Accepted Spring 2025 applicants GPA"""
    query = """
    SELECT AVG(gpa) as avg_gpa
    FROM applicants 
    WHERE term = 'Spring 2025' AND status = 'Accepted' AND gpa IS NOT NULL
    """
    result = execute_query(query)
    
    return {
        'question': 'What is the average GPA of applicants who applied for Spring 2025 who are Acceptances?',
        'answer': round(result[0][0], 3) if result and result[0][0] else 0,
        'query': query.strip(),
        'explanation': 'Average GPA of successful Spring 2025 applicants'
    }

def get_jhu_cs_masters_count():
    """Query 7: JHU Computer Science masters applications"""
    query = """
    SELECT COUNT(*) as count
    FROM applicants 
    WHERE program LIKE '%Johns Hopkins%Computer Science%' 
        AND (degree LIKE '%MS%' OR degree LIKE '%Master%')
    """
    result = execute_query(query)
    
    return {
        'question': 'How many entries are from applicants who applied to JHU for a masters degree in Computer Science?',
        'answer': result[0][0] if result else 0,
        'query': query.strip(),
        'explanation': 'Count of JHU CS masters program applications'
    }

def get_all_analysis_results():
    """Compile all analysis results"""
    try:
        query_1 = get_spring_2025_entries()
        query_2 = get_international_percentage()
        query_3 = get_average_scores()
        query_4 = get_american_spring_2025_gpa()
        query_5 = get_spring_2025_acceptance_rate()
        query_6 = get_accepted_spring_2025_gpa()
        query_7 = get_jhu_cs_masters_count()
        
        return {
            'spring_2025_count': query_1.get('answer', 0),
            'international_percentage': query_2.get('answer', 0),
            'average_scores': query_3.get('answer', {}),
            'american_spring_2025_gpa': query_4.get('answer', 0),
            'spring_2025_acceptance_rate': query_5.get('answer', 0),
            'accepted_spring_2025_gpa': query_6.get('answer', 0),
            'jhu_cs_masters_count': query_7.get('answer', 0),
            'detailed_results': {
                'spring_2025_entries': query_1,
                'international_percentage': query_2,
                'average_scores': query_3,
                'american_spring_2025_gpa': query_4,
                'spring_2025_acceptance_rate': query_5,
                'accepted_spring_2025_gpa': query_6,
                'jhu_cs_masters_count': query_7
            },
            'metadata': {
                'database_type': 'SQLite',
                'author': 'Abdullateef Mumin'
            }
        }
    except Exception as e:
        logger.error(f"Error compiling results: {e}")
        return {'error': str(e)}

@app.route('/')
def index():
    """Main dashboard route"""
    try:
        results = get_all_analysis_results()
        return render_template('index.html', results=results)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return render_template('index.html', error=str(e))

@app.route('/api/results')
def api_results():
    """JSON API endpoint"""
    try:
        results = get_all_analysis_results()
        return jsonify(results)
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'database': 'SQLite',
        'author': 'Abdullateef Mumin'
    })

if __name__ == '__main__':
    # Verify SQLite database exists
    if not os.path.exists(SQLITE_DB_PATH):
        logger.error(f"SQLite database not found: {SQLITE_DB_PATH}")
        print("Error: gradcafe.db not found. Please ensure the database file is present.")
        exit(1)
    
    print("=" * 60)
    print("Graduate School Data Analysis - SQLite Version")
    print("Author: Abdullateef Mumin")
    print("=" * 60)
    print("Starting SQLite application server...")
    print("Access at: http://localhost:5001")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=True)