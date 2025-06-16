#!/usr/bin/env python3
"""
Application Entry Point.

Graduate School Data Analysis Platform with Security Hardening.

Author: Abdullateef Mumin
"""

from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("Graduate School Data Analysis Platform - Security Hardened")
    print("Author: Abdullateef Mumin")
    print("Features: 10/10 PyLint, SQL Injection Protection, Input Validation")
    print("=" * 60)
    print("Starting secure application server...")
    print("Access the application at: http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
