#!/usr/bin/env python3
"""
Application Entry Point
Graduate School Data Analysis Platform

Author: Abdullateef Mumin

Simple entry point that launches the Flask web application.
Run this file to start the server and access the analysis dashboard.
Compatible with both PostgreSQL and SQLite database backends.
"""
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("Graduate School Data Analysis Platform")
    print("Author: Abdullateef Mumin")

    print("=" * 60)
    print("Starting application server...")
    print("Access the application at: http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)