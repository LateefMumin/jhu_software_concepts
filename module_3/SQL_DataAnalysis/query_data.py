"""
SQL Query Implementation for Graduate School Data Analysis

This module contains seven analytical SQL queries that examine graduate school
admission patterns, demographics, and academic performance metrics from the
grad cafe dataset. Each query addresses specific research questions about
Spring 2025 admissions.

Author: Abdullateef Mumin

Implementation uses PostgreSQL with SQLAlchemy ORM for database operations,
with comprehensive error handling and logging for production reliability.
"""

import logging
from sqlalchemy import text
from app import app, db

# Configure logging for query monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_spring_2025_entries():
    """
    Query 1: Count of Spring 2025 Applications
    
    Research Question: How many entries do you have in your database 
    who have applied for Spring 2025?
    
    This analysis examines the total volume of graduate school applications
    submitted for the Spring 2025 academic term across all programs and institutions
    in the dataset. Understanding application volume helps identify admission trends.
    
    Returns:
        dict: Query results with count, SQL, and metadata
    """
    try:
        with app.app_context():
            # Direct SQL query for precise control and transparency
            query_text = "SELECT COUNT(*) FROM applicants WHERE term = 'Spring 2025'"
            result = db.session.execute(text(query_text)).scalar()
            
            logger.info(f"Spring 2025 applications query executed: {result} records found")
            
            return {
                'question': 'How many entries do you have in your database who have applied for Spring 2025?',
                'answer': result or 0,
                'query': query_text,
                'explanation': 'This query counts all applicant records where the term field equals "Spring 2025"',
                'methodology': 'Simple COUNT aggregation with WHERE clause filtering'
            }
    except Exception as e:
        logger.error(f"Error in Spring 2025 entries query: {str(e)}")
        return {'error': f"Database query failed: {str(e)}"}

def get_international_percentage():
    """
    Query 2: International Student Percentage Analysis
    
    Research Question: What percentage of entries are from international students?
    
    This analysis calculates the demographic distribution of applicants by examining
    the proportion of international versus domestic students. This metric is crucial
    for understanding the global reach and diversity of graduate programs.
    
    Returns:
        dict: Percentage of international students with detailed breakdown
    """
    try:
        with app.app_context():
            # Calculate percentage using conditional aggregation
            query_text = """
            SELECT 
                COUNT(CASE WHEN us_or_international = 'International' THEN 1 END) * 100.0 / COUNT(*) as intl_percentage,
                COUNT(CASE WHEN us_or_international = 'International' THEN 1 END) as intl_count,
                COUNT(*) as total_count
            FROM applicants 
            WHERE us_or_international IS NOT NULL
            """
            result = db.session.execute(text(query_text)).fetchone()
            
            if result:
                percentage = round(float(result[0]), 2) if result[0] else 0
                intl_count = int(result[1]) if result[1] else 0
                total = int(result[2]) if result[2] else 0
                
                logger.info(f"International percentage query: {percentage}% ({intl_count}/{total})")
                
                return {
                    'question': 'What percentage of entries are from international students?',
                    'answer': f"{percentage}%",
                    'international_count': intl_count,
                    'total_count': total,
                    'query': query_text.strip(),
                    'explanation': f'Calculated from {total} applicants with nationality data: {intl_count} international students',
                    'methodology': 'Conditional COUNT with percentage calculation using CASE WHEN'
                }
            else:
                return {
                    'question': 'What percentage of entries are from international students?',
                    'answer': '0%',
                    'query': query_text.strip(),
                    'explanation': 'No nationality data available for analysis'
                }
    except Exception as e:
        logger.error(f"Error in international percentage query: {str(e)}")
        return {'error': f"International percentage calculation failed: {str(e)}"}

def get_average_scores():
    """
    Query 3: Academic Performance Metrics Analysis
    
    Research Question: What is the average GPA, GRE, GRE V, GRE AW of applicants 
    who provide these metrics?
    
    This comprehensive analysis examines the academic qualifications of applicants
    by calculating mean values for all standardized metrics. Only includes applicants
    who provided complete data to ensure statistical validity.
    
    Returns:
        dict: Average scores for all academic metrics
    """
    try:
        with app.app_context():
            query_text = """
            SELECT 
                AVG(gpa) as avg_gpa,
                AVG(gre) as avg_gre,
                AVG(gre_v) as avg_gre_v,
                AVG(gre_aw) as avg_gre_aw,
                COUNT(*) as complete_records
            FROM applicants 
            WHERE gpa IS NOT NULL 
                AND gre IS NOT NULL 
                AND gre_v IS NOT NULL 
                AND gre_aw IS NOT NULL
            """
            result = db.session.execute(text(query_text)).fetchone()
            
            if result and result[0] is not None:
                avg_scores = {
                    'avg_gpa': round(float(result[0]), 3),
                    'avg_gre': round(float(result[1]), 1),
                    'avg_gre_v': round(float(result[2]), 1),
                    'avg_gre_aw': round(float(result[3]), 2)
                }
                count = int(result[4])
                
                logger.info(f"Average scores calculated for {count} complete records")
                
                return {
                    'question': 'What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?',
                    'answer': avg_scores,
                    'query': query_text.strip(),
                    'explanation': 'Calculates mean values for all academic metrics, excluding incomplete records',
                    'methodology': 'AVG aggregation with comprehensive NULL filtering for data quality'
                }
            else:
                return {
                    'question': 'What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?',
                    'answer': {'avg_gpa': 0, 'avg_gre': 0, 'avg_gre_v': 0, 'avg_gre_aw': 0},
                    'query': query_text.strip(),
                    'explanation': 'No complete academic records available for analysis'
                }
    except Exception as e:
        logger.error(f"Error in average scores query: {str(e)}")
        return {'error': f"Average scores calculation failed: {str(e)}"}

def get_american_spring_2025_gpa():
    """
    Query 4: Domestic Student Academic Performance
    
    Research Question: What is the average GPA of American students in Spring 2025?
    
    This targeted analysis focuses on the academic performance of domestic students
    applying for Spring 2025 admission, providing insights into competitive
    standards for American applicants in the current admission cycle.
    
    Returns:
        dict: Average GPA for American Spring 2025 applicants
    """
    try:
        with app.app_context():
            query_text = """
            SELECT 
                AVG(gpa) as avg_gpa,
                COUNT(*) as american_spring_count
            FROM applicants 
            WHERE us_or_international = 'American' 
                AND term = 'Spring 2025' 
                AND gpa IS NOT NULL
            """
            result = db.session.execute(text(query_text)).fetchone()
            
            if result and result[0] is not None:
                avg_gpa = round(float(result[0]), 3)
                count = int(result[1])
                
                logger.info(f"American Spring 2025 GPA: {avg_gpa} (n={count})")
                
                return {
                    'question': 'What is the average GPA of American students in Spring 2025?',
                    'answer': avg_gpa,
                    'sample_size': count,
                    'query': query_text.strip(),
                    'explanation': 'Calculates mean GPA for domestic students applying Spring 2025',
                    'methodology': 'Filtered AVG aggregation with demographic and term constraints'
                }
            else:
                return {
                    'question': 'What is the average GPA of American students in Spring 2025?',
                    'answer': 0,
                    'query': query_text.strip(),
                    'explanation': 'No American Spring 2025 applicants with GPA data found'
                }
    except Exception as e:
        logger.error(f"Error in American Spring 2025 GPA query: {str(e)}")
        return {'error': f"American GPA calculation failed: {str(e)}"}

def get_spring_2025_acceptance_rate():
    """
    Query 5: Spring 2025 Admission Success Analysis
    
    Research Question: What percent of entries for Spring 2025 are Acceptances?
    
    This critical analysis examines admission outcomes for the Spring 2025 cycle,
    calculating the overall acceptance rate to understand admission competitiveness
    and success rates across all programs and institutions.
    
    Returns:
        dict: Acceptance rate percentage with detailed breakdown
    """
    try:
        with app.app_context():
            query_text = """
            SELECT 
                COUNT(CASE WHEN status = 'Accepted' THEN 1 END) * 100.0 / COUNT(*) as acceptance_rate,
                COUNT(CASE WHEN status = 'Accepted' THEN 1 END) as accepted_count,
                COUNT(*) as total_spring_2025
            FROM applicants 
            WHERE term = 'Spring 2025'
            """
            result = db.session.execute(text(query_text)).fetchone()
            
            if result:
                acceptance_rate = round(float(result[0]), 2) if result[0] else 0
                accepted_count = int(result[1]) if result[1] else 0
                total_count = int(result[2]) if result[2] else 0
                
                logger.info(f"Spring 2025 acceptance rate: {acceptance_rate}% ({accepted_count}/{total_count})")
                
                return {
                    'question': 'What percent of entries for Spring 2025 are Acceptances?',
                    'answer': f"{acceptance_rate}%",
                    'accepted_count': accepted_count,
                    'total_count': total_count,
                    'query': query_text.strip(),
                    'explanation': f'Acceptance rate calculated from {total_count} Spring 2025 applications with {accepted_count} acceptances',
                    'methodology': 'Conditional aggregation using CASE WHEN for percentage calculation'
                }
            else:
                return {
                    'question': 'What percent of entries for Spring 2025 are Acceptances?',
                    'answer': '0%',
                    'query': query_text.strip(),
                    'explanation': 'No Spring 2025 records found for analysis'
                }
    except Exception as e:
        logger.error(f"Error in Spring 2025 acceptance rate query: {str(e)}")
        return {'error': f"Acceptance rate calculation failed: {str(e)}"}

def get_accepted_spring_2025_gpa():
    """
    Query 6: Successful Applicant Academic Profile
    
    Research Question: What is the average GPA of applicants who applied for 
    Spring 2025 who are Acceptances?
    
    This analysis examines the academic profile of successful Spring 2025 applicants,
    providing insights into the GPA standards required for admission and helping
    understand the academic threshold for acceptance.
    
    Returns:
        dict: Average GPA of accepted Spring 2025 applicants
    """
    try:
        with app.app_context():
            query_text = """
            SELECT 
                AVG(gpa) as avg_accepted_gpa,
                COUNT(*) as accepted_spring_count
            FROM applicants 
            WHERE term = 'Spring 2025' 
                AND status = 'Accepted' 
                AND gpa IS NOT NULL
            """
            result = db.session.execute(text(query_text)).fetchone()
            
            if result and result[0] is not None:
                avg_gpa = round(float(result[0]), 3)
                count = int(result[1])
                
                logger.info(f"Accepted Spring 2025 GPA: {avg_gpa} (n={count})")
                
                return {
                    'question': 'What is the average GPA of applicants who applied for Spring 2025 who are Acceptances?',
                    'answer': avg_gpa,
                    'accepted_count': count,
                    'query': query_text.strip(),
                    'explanation': f'Average GPA calculated from {count} accepted Spring 2025 applicants with GPA data',
                    'methodology': 'AVG aggregation with dual filtering for term and admission status'
                }
            else:
                return {
                    'question': 'What is the average GPA of applicants who applied for Spring 2025 who are Acceptances?',
                    'answer': 0,
                    'query': query_text.strip(),
                    'explanation': 'No accepted Spring 2025 applicants with GPA data found'
                }
    except Exception as e:
        logger.error(f"Error in accepted Spring 2025 GPA query: {str(e)}")
        return {'error': f"Accepted GPA calculation failed: {str(e)}"}

def get_jhu_cs_masters_count():
    """
    Query 7: Johns Hopkins Computer Science Program Analysis
    
    Research Question: How many entries are from applicants who applied to JHU 
    for a masters degree in Computer Science?
    
    This institutional analysis focuses specifically on Johns Hopkins University
    Computer Science masters programs, using pattern matching to identify
    relevant applications and understand program-specific application volume.
    
    Returns:
        dict: Count of JHU CS masters applications
    """
    try:
        with app.app_context():
            query_text = """
            SELECT COUNT(*) as jhu_cs_masters_count
            FROM applicants 
            WHERE (LOWER(program) LIKE '%johns hopkins%' OR LOWER(program) LIKE '%jhu%')
                AND LOWER(program) LIKE '%computer science%'
                AND LOWER(degree) LIKE '%master%'
            """
            result = db.session.execute(text(query_text)).scalar()
            count = result if result else 0
            
            logger.info(f"JHU CS Masters applications: {count}")
            
            return {
                'question': 'How many entries are from applicants who applied to JHU for a masters degree in Computer Science?',
                'answer': count,
                'query': query_text,
                'explanation': f'Pattern matching identified {count} applications to Johns Hopkins Computer Science masters programs',
                'methodology': 'LIKE pattern matching with case-insensitive string comparison'
            }
    except Exception as e:
        logger.error(f"Error in JHU CS masters query: {str(e)}")
        return {'error': f"JHU CS masters count failed: {str(e)}"}

def get_all_analysis_results():
    """
    Comprehensive Analysis Results Aggregation
    
    Executes all seven analytical queries and compiles results into a unified
    data structure suitable for web presentation and API responses. Includes
    error handling and summary statistics for the complete dataset.
    
    Returns:
        dict: Complete analysis results with all query outputs and metadata
    """
    try:
        logger.info("Starting comprehensive analysis of graduate school data...")
        
        # Execute all analytical queries
        results = {
            'spring_2025_entries': get_spring_2025_entries(),
            'international_percentage': get_international_percentage(),
            'average_scores': get_average_scores(),
            'american_spring_2025_gpa': get_american_spring_2025_gpa(),
            'spring_2025_acceptance_rate': get_spring_2025_acceptance_rate(),
            'accepted_spring_2025_gpa': get_accepted_spring_2025_gpa(),
            'jhu_cs_masters_count': get_jhu_cs_masters_count()
        }
        
        # Calculate summary statistics
        total_records = results['spring_2025_entries'].get('answer', 0)
        analysis_summary = {
            'total_records': total_records,
            'analysis_date': '2024-12-08',
            'queries_executed': 7,
            'data_source': 'Graduate School Applications Database',
            'focus_term': 'Spring 2025'
        }
        
        results['summary'] = analysis_summary
        logger.info(f"Analysis completed successfully for {total_records} total records")
        
        return results
        
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {str(e)}")
        return {'error': f"Analysis compilation failed: {str(e)}"}

def main():
    """
    Main function for standalone query testing and validation
    
    Executes all queries individually and displays results for debugging
    and verification purposes. Useful for development and testing.
    """
    print("Graduate School Data Analysis")
    print("JHU EP 605.256 Module 3 Assignment")
    print("=" * 80)
    
    # List of all analytical functions
    queries = [
        ("Query 1: Spring 2025 Applications", get_spring_2025_entries),
        ("Query 2: International Percentage", get_international_percentage),
        ("Query 3: Average Academic Scores", get_average_scores),
        ("Query 4: American Spring 2025 GPA", get_american_spring_2025_gpa),
        ("Query 5: Spring 2025 Acceptance Rate", get_spring_2025_acceptance_rate),
        ("Query 6: Accepted Spring 2025 GPA", get_accepted_spring_2025_gpa),
        ("Query 7: JHU CS Masters Count", get_jhu_cs_masters_count)
    ]
    
    # Execute each query and display results
    for i, (description, query_func) in enumerate(queries, 1):
        print(f"\n{description}")
        print("-" * 60)
        try:
            result = query_func()
            if 'error' in result:
                print(f"ERROR: {result['error']}")
            else:
                print(f"Question: {result.get('question', 'N/A')}")
                print(f"Answer: {result.get('answer', 'N/A')}")
                print(f"SQL: {result.get('query', 'N/A')}")
        except Exception as e:
            print(f"EXCEPTION: {str(e)}")
    
    print("\n" + "=" * 80)
    print("Analysis Complete")

if __name__ == "__main__":
    main()