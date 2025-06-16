# Graduate School Data Analysis Platform - Security Hardened

**Author: Abdullateef Mumin**

A comprehensive Flask web application analyzing graduate school admission trends using PostgreSQL database operations with advanced security hardening, 10/10 PyLint compliance, and SQL injection protection.

## 🔒 Security Features

- **10/10 PyLint Rating:** Zero errors, complete code quality compliance
- **SQL Injection Protection:** psycopg2 sql.SQL composition methods
- **Input Validation:** Comprehensive sanitization and validation
- **Query Limits:** All SQL queries include LIMIT clauses
- **Parameterized Queries:** No string concatenation in SQL
- **Error Handling:** Secure error messages without information leakage

## 🚀 Quick Start

### Option 1: Secure SQLite Setup (Recommended for Testing)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the secure SQLite version
python app_sqlite.py
