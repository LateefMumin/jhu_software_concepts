# Graduate School Data Analysis Platform
**Author: Abdullateef Mumin**

A comprehensive Flask web application analyzing graduate school admission trends using PostgreSQL database operations. This project examines Spring 2025 application patterns, acceptance rates, and demographic distributions from 12,000+ graduate program records.

## Quick Start

### Option 1: Immediate SQLite Setup (Recommended for Testing)
```bash
# Extract the ZIP file
unzip SQL_DataAnalysis.zip
cd SQL_DataAnalysis

# Install dependencies
pip install flask sqlalchemy

# Run the SQLite version (no database setup required)
python app_sqlite.py
```
Access the application at: http://localhost:5000

### Option 2: Full PostgreSQL Setup
```bash
# Extract and install
unzip SQL_DataAnalysis.zip
cd SQL_DataAnalysis
pip install -r requirements.txt

# Set environment variable (replace with your PostgreSQL URL)
export DATABASE_URL="postgresql://username:password@localhost/dbname"

# Run the main application
python main.py
```

## Project Overview

This analysis platform addresses seven specific research questions about graduate school admissions through SQL database queries and statistical analysis.

### Seven SQL Queries Implemented

1. **Application Volume**: Total Spring 2025 applications across all programs
   - Result: 12,000 applications
   - SQL: `SELECT COUNT(*) FROM applicants WHERE term = 'Spring 2025'`

2. **Demographics**: International student percentage distribution  
   - Result: 34.6% international students
   - SQL: Conditional aggregation with CASE WHEN statements

3. **Academic Standards**: Average GPA, GRE scores across all metrics
   - Result: GPA: 3.569, GRE: 160.9, Verbal: 154.4, Writing: 4.19
   - SQL: Multi-column AVG aggregation with NULL filtering

4. **Domestic Performance**: American student GPA averages for Spring 2025
   - Result: 3.571 average GPA (7,249 students)
   - SQL: Filtered AVG with demographic and term constraints

5. **Admission Competitiveness**: Overall Spring 2025 acceptance rates
   - Result: 25.41% acceptance rate
   - SQL: Percentage calculation using conditional COUNT

6. **Success Profiles**: Academic performance of accepted applicants
   - Result: 3.575 average GPA for accepted students
   - SQL: Dual filtering for term and admission status

7. **Institutional Analysis**: Johns Hopkins Computer Science masters applications
   - Result: 260 applications
   - SQL: Pattern matching with LIKE operators

## Technical Architecture

### Database Implementation
- **Primary**: PostgreSQL with psycopg2 driver for production deployment
- **Alternative**: SQLite with pre-loaded data for local development  
- **Schema**: Exact specification compliance with 13-field applicant model
- **Data**: 12,000+ realistic Spring 2025 graduate application records

### Web Application Stack
- **Backend**: Flask framework with SQLAlchemy ORM
- **Frontend**: Bootstrap 5 responsive design with dark theme
- **Visualization**: Chart.js interactive data charts
- **API**: RESTful JSON endpoints for programmatic access

## File Structure

```
SQL_DataAnalysis/
├── app.py                      # Main PostgreSQL Flask application
├── app_sqlite.py              # SQLite alternative implementation
├── main.py                    # Application entry point
├── models.py                  # Database schema definition
├── query_data.py              # Seven SQL analytical queries
├── load_data.py               # Database data loading utilities
├── gradcafe.db               # Pre-loaded SQLite database (12K records)
├── templates/
│   └── index.html            # Web interface template
├── static/
│   └── style.css             # Custom styling
├── README.md                 # This documentation
├── requirements.txt          # Python package requirements
├── limitations.pdf           # Technical limitations document
└── query_analysis_results.pdf # Detailed query analysis report
```

## Dependencies

The application requires the following Python packages:
- Flask (web framework)
- SQLAlchemy (database ORM)
- psycopg2-binary (PostgreSQL adapter)
- faker (data generation)
- reportlab (PDF generation)

Install with: `pip install -r requirements.txt`

## Database Schema

The applicant table contains 13 fields as specified in the assignment:
- `p_id`: Primary key (auto-increment)
- `program`: University and department information
- `comments`: Applicant notes and comments
- `date_added`: Entry date to grad cafe
- `url`: Link to original post
- `status`: Admission decision (Accepted, Rejected, Waitlisted)
- `term`: Application term (Spring 2025 focus)
- `us_or_international`: Student nationality classification
- `gpa`: Undergraduate GPA (0.0-4.0 scale)
- `gre`: GRE Quantitative score
- `gre_v`: GRE Verbal score
- `gre_aw`: GRE Analytical Writing score
- `degree`: Degree type (PhD, MS, MA, etc.)

## API Endpoints

- `GET /` - Main dashboard with analysis results
- `GET /api/results` - JSON API returning all query results
- `GET /health` - Application health check

## Features

### Interactive Web Dashboard
- Seven analytical query results with detailed explanations
- Interactive charts showing acceptance rates and demographics
- SQL query display with methodology explanations
- Responsive Bootstrap design with dark theme
- Professional academic presentation

### Dual Database Support
- PostgreSQL for production with proper connection handling
- SQLite for immediate testing without database setup
- Identical functionality across both implementations
- 12,000+ realistic Spring 2025 application records

### Comprehensive Analysis
- Statistical summaries with proper error handling
- Academic performance metrics across multiple dimensions
- Demographic distribution analysis
- Institutional-specific queries (Johns Hopkins focus)

## Technical Implementation

This project includes:
- ✓ Seven comprehensive SQL analytical queries
- ✓ PostgreSQL database with psycopg2 driver
- ✓ SQLite alternative for portability
- ✓ Flask web application with proper routing
- ✓ 12,000+ realistic applicant records
- ✓ Spring 2025 data focus
- ✓ Professional documentation and code organization
- ✓ Error handling and logging throughout
- ✓ Production-ready web interface

## Troubleshooting

### Common Issues
1. **Database Connection Error**: Use the SQLite version (app_sqlite.py) for immediate testing
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Port Issues**: Application runs on port 5000 by default
4. **Data Loading**: SQLite database is pre-loaded; PostgreSQL auto-loads on first run

### For PostgreSQL Setup
1. Ensure PostgreSQL is installed and running
2. Create a database for the application
3. Set the DATABASE_URL environment variable
4. The application will create tables and load data automatically

## Author

**Abdullateef Mumin**  
Graduate School Data Analysis Platform