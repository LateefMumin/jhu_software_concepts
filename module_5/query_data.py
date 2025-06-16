"""
Secure SQL Query Implementation for Graduate School Data Analysis.

This module contains seven analytical SQL queries using psycopg's sql module
for secure query composition and SQL injection prevention.

Author: Abdullateef Mumin
"""

import logging
from typing import Dict, Any, Optional
import psycopg2
from psycopg2 import sql
from app import app
from security_utils import InputValidator

# Configure logging for query monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecureQueryExecutor:
    """Secure database query executor with comprehensive error handling."""

    def __init__(self):
        """Initialize the query executor."""
        self.connection = None

    def get_connection(self):
        """Get secure database connection."""
        try:
            database_url = app.config["SQLALCHEMY_DATABASE_URI"]
            self.connection = psycopg2.connect(database_url)
            return self.connection
        except Exception as exc:
            logger.error("Database connection error: %s", exc)
            raise

    def execute_secure_query(self, query: sql.Composed) -> Optional[Any]:
        """
        Execute a secure SQL query with proper error handling.

        Args:
            query: Secure SQL query object

        Returns:
            Optional[Any]: Query results or None if error
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()

            cursor.close()
            conn.close()

            return result
        except Exception as exc:
            logger.error("Query execution error: %s", exc)
            if self.connection:
                self.connection.close()
            raise

    def execute_single_result_query(self, query: sql.Composed) -> Optional[Any]:
        """
        Execute query expecting single result.

        Args:
            query: Secure SQL query object

        Returns:
            Optional[Any]: Single query result or None
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchone()

            cursor.close()
            conn.close()

            return result
        except Exception as exc:
            logger.error("Single result query error: %s", exc)
            if self.connection:
                self.connection.close()
            raise


def get_spring_2025_entries() -> Dict[str, Any]:
    """
    Query 1: Count of Spring 2025 Applications.

    Research Question: How many entries do you have in your database
    who have applied for Spring 2025?

    Returns:
        Dict[str, Any]: Query results with count, SQL, and metadata
    """
    try:
        # Validate input
        term = "Spring 2025"
        if not InputValidator.validate_term(term):
            return {'error': 'Invalid term format'}

        # Build secure query
        query = sql.SQL("""
            SELECT COUNT(*) as count
            FROM {table}
            WHERE {field} = {value}
            LIMIT 1
        """).format(
            table=sql.Identifier('applicants'),
            field=sql.Identifier('term'),
            value=sql.Literal(term)
        )

        # Execute query
        executor = SecureQueryExecutor()
        result = executor.execute_single_result_query(query)

        count = result[0] if result else 0
        logger.info("Spring 2025 applications query executed: %s records found", count)

        return {
            'question': 'How many entries do you have in your database who have applied for Spring 2025?',
            'answer': count,
            'query': 'SELECT COUNT(*) FROM applicants WHERE term = %s LIMIT 1',
            'explanation': 'This query counts all applicant records where the term field equals "Spring 2025"',
            'methodology': 'Simple COUNT aggregation with WHERE clause filtering and LIMIT protection'
        }
    except Exception as exc:
        logger.error("Error in Spring 2025 entries query: %s", exc)
        return {'error': f"Database query failed: {str(exc)}"}


def get_international_percentage() -> Dict[str, Any]:
    """
    Query 2: International Student Percentage Analysis.

    Research Question: What percentage of entries are from international students?

    Returns:
        Dict[str, Any]: Percentage of international students with detailed breakdown
    """
    try:
        # Validate input
        nationality = "International"
        if not InputValidator.validate_nationality(nationality):
            return {'error': 'Invalid nationality value'}

        # Build secure query
        query = sql.SQL("""
            SELECT
                COUNT(CASE WHEN {field} = {value} THEN 1 END) * 100.0 / COUNT(*) as percentage,
                COUNT(CASE WHEN {field} = {value} THEN 1 END) as match_count,
                COUNT(*) as total_count
            FROM {table}
            WHERE {field} IS NOT NULL
            LIMIT 1
        """).format(
            field=sql.Identifier('us_or_international'),
            value=sql.Literal(nationality),
            table=sql.Identifier('applicants')
        )

        # Execute query
        executor = SecureQueryExecutor()
        result = executor.execute_single_result_query(query)

        if result:
            percentage = round(float(result[0]), 2) if result[0] else 0
            intl_count = int(result[1]) if result[1] else 0
            total = int(result[2]) if result[2] else 0

            logger.info("International percentage query: %s%% (%s/%s)", percentage, intl_count, total)

            return {
                'question': 'What percentage of entries are from international students?',
                'answer': f"{percentage}%",
                'international_count': intl_count,
                'total_count': total,
                'query': 'SELECT COUNT(CASE WHEN us_or_international = %s THEN 1 END) * 100.0 / COUNT(*) FROM applicants WHERE us_or_international IS NOT NULL LIMIT 1',
                'explanation': f'Calculated from {total} applicants with nationality data: {intl_count} international students',
                'methodology': 'Conditional COUNT with percentage calculation using CASE WHEN and LIMIT protection'
            }
        else:
            return {
                'question': 'What percentage of entries are from international students?',
                'answer': '0%',
                'query': 'SELECT COUNT(CASE WHEN us_or_international = %s THEN 1 END) * 100.0 / COUNT(*) FROM applicants WHERE us_or_international IS NOT NULL LIMIT 1',
                'explanation': 'No nationality data available for analysis'
            }
    except Exception as exc:
        logger.error("Error in international percentage query: %s", exc)
        return {'error': f"International percentage calculation failed: {str(exc)}"}


def get_average_scores() -> Dict[str, Any]:
    """
    Query 3: Academic Performance Metrics Analysis.

    Research Question: What is the average GPA, GRE, GRE V, GRE AW of applicants
    who provide these metrics?

    Returns:
        Dict[str, Any]: Average scores for all academic metrics
    """
    try:
        # Build secure query for multiple averages
        query = sql.SQL("""
            SELECT
                AVG({gpa}) as avg_gpa,
                AVG({gre}) as avg_gre,
                AVG({gre_v}) as avg_gre_v,
                AVG({gre_aw}) as avg_gre_aw
            FROM {table}
            WHERE {gpa} IS NOT NULL
                AND {gre} IS NOT NULL
                AND {gre_v} IS NOT NULL
                AND {gre_aw} IS NOT NULL
            LIMIT 1
        """).format(
            gpa=sql.Identifier('gpa'),
            gre=sql.Identifier('gre'),
            gre_v=sql.Identifier('gre_v'),
            gre_aw=sql.Identifier('gre_aw'),
            table=sql.Identifier('applicants')
        )

        # Execute query
        executor = SecureQueryExecutor()
        result = executor.execute_single_result_query(query)

        if result and result[0] is not None:
            avg_scores = {
                'avg_gpa': round(float(result[0]), 3),
                'avg_gre': round(float(result[1]), 1),
                'avg_gre_v': round(float(result[2]), 1),
                'avg_gre_aw': round(float(result[3]), 2)
            }

            logger.info("Average scores calculated successfully")

            return {
                'question': 'What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?',
                'answer': avg_scores,
                'query': 'SELECT AVG(gpa), AVG(gre), AVG(gre_v), AVG(gre_aw) FROM applicants WHERE gpa IS NOT NULL AND gre IS NOT NULL AND gre_v IS NOT NULL AND gre_aw IS NOT NULL LIMIT 1',
                'explanation': 'Calculates mean values for all academic metrics, excluding incomplete records',
                'methodology': 'AVG aggregation with comprehensive NULL filtering and LIMIT protection'
            }
        else:
            return {
                'question': 'What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?',
                'answer': {'avg_gpa': 0, 'avg_gre': 0, 'avg_gre_v': 0, 'avg_gre_aw': 0},
                'query': 'SELECT AVG(gpa), AVG(gre), AVG(gre_v), AVG(gre_aw) FROM applicants WHERE gpa IS NOT NULL AND gre IS NOT NULL AND gre_v IS NOT NULL AND gre_aw IS NOT NULL LIMIT 1',
                'explanation': 'No complete academic records available for analysis'
            }
    except Exception as exc:
        logger.error("Error in average scores query: %s", exc)
        return {'error': f"Average scores calculation failed: {str(exc)}"}


def get_american_spring_2025_gpa() -> Dict[str, Any]:
    """
    Query 4: Domestic Student Academic Performance.

    Research Question: What is the average GPA of American students in Spring 2025?

    Returns:
        Dict[str, Any]: Average GPA for American Spring 2025 applicants
    """
    try:
        # Validate inputs
        nationality = "American"
        term = "Spring 2025"

        if not InputValidator.validate_nationality(nationality):
            return {'error': 'Invalid nationality value'}
        if not InputValidator.validate_term(term):
            return {'error': 'Invalid term format'}

        # Build secure query
        query = sql.SQL("""
            SELECT AVG({gpa}) as avg_gpa
            FROM {table}
            WHERE {nationality_field} = {nationality}
                AND {term_field} = {term}
                AND {gpa} IS NOT NULL
            LIMIT 1
        """).format(
            gpa=sql.Identifier('gpa'),
            table=sql.Identifier('applicants'),
            nationality_field=sql.Identifier('us_or_international'),
            term_field=sql.Identifier('term'),
            nationality=sql.Literal(nationality),
            term=sql.Literal(term)
        )

        # Execute query
        executor = SecureQueryExecutor()
        result = executor.execute_single_result_query(query)

        if result and result[0] is not None:
            avg_gpa = round(float(result[0]), 3)

            logger.info("American Spring 2025 GPA: %s", avg_gpa)

            return {
                'question': 'What is the average GPA of American students in Spring 2025?',
                'answer': avg_gpa,
                'query': 'SELECT AVG(gpa) FROM applicants WHERE us_or_international = %s AND term = %s AND gpa IS NOT NULL LIMIT 1',
                'explanation': 'Calculates mean GPA for domestic students applying Spring 2025',
                'methodology': 'Filtered AVG aggregation with demographic and term constraints plus LIMIT protection'
            }
        else:
            return {
                'question': 'What is the average GPA of American students in Spring 2025?',
                'answer': 0,
                'query': 'SELECT AVG(gpa) FROM applicants WHERE us_or_international = %s AND term = %s AND gpa IS NOT NULL LIMIT 1',
                'explanation': 'No American Spring 2025 applicants with GPA data found'
            }
    except Exception as exc:
        logger.error("Error in American Spring 2025 GPA query: %s", exc)
        return {'error': f"American GPA calculation failed: {str(exc)}"}


def get_spring_2025_acceptance_rate() -> Dict[str, Any]:
    """
    Query 5: Spring 2025 Admission Success Analysis.

    Research Question: What percent of entries for Spring 2025 are Acceptances?

    Returns:
        Dict[str, Any]: Acceptance rate percentage with detailed breakdown
    """
    try:
        # Validate inputs
        term = "Spring 2025"
        status = "Accepted"

        if not InputValidator.validate_term(term):
            return {'error': 'Invalid term format'}
        if not InputValidator.validate_status(status):
            return {'error': 'Invalid status value'}

        # Build secure query
        query = sql.SQL("""
            SELECT
                COUNT(CASE WHEN {status_field} = {status} THEN 1 END) * 100.0 / COUNT(*) as acceptance_rate,
                COUNT(CASE WHEN {status_field} = {status} THEN 1 END) as accepted_count,
                COUNT(*) as total_spring_2025
            FROM {table}
            WHERE {term_field} = {term}
            LIMIT 1
        """).format(
            status_field=sql.Identifier('status'),
            term_field=sql.Identifier('term'),
            table=sql.Identifier('applicants'),
            status=sql.Literal(status),
            term=sql.Literal(term)
        )

        # Execute query
        executor = SecureQueryExecutor()
        result = executor.execute_single_result_query(query)

        if result:
            acceptance_rate = round(float(result[0]), 2) if result[0] else 0
            accepted_count = int(result[1]) if result[1] else 0
            total_count = int(result[2]) if result[2] else 0

            logger.info("Spring 2025 acceptance rate: %s%% (%s/%s)", acceptance_rate, accepted_count, total_count)

            return {
                'question': 'What percent of entries for Spring 2025 are Acceptances?',
                'answer': f"{acceptance_rate}%",
                'accepted_count': accepted_count,
                'total_count': total_count,
                'query': 'SELECT COUNT(CASE WHEN status = %s THEN 1 END) * 100.0 / COUNT(*) FROM applicants WHERE term = %s LIMIT 1',
                'explanation': f'Acceptance rate calculated from {total_count} Spring 2025 applications with {accepted_count} acceptances',
                'methodology': 'Conditional aggregation using CASE WHEN for percentage calculation with LIMIT protection'
            }
        else:
            return {
                'question': 'What percent of entries for Spring 2025 are Acceptances?',
                'answer': '0%',
                'query': 'SELECT COUNT(CASE WHEN status = %s THEN 1 END) * 100.0 / COUNT(*) FROM applicants WHERE term = %s LIMIT 1',
                'explanation': 'No Spring 2025 records found for analysis'
            }
    except Exception as exc:
        logger.error("Error in Spring 2025 acceptance rate query: %s", exc)
        return {'error': f"Acceptance rate calculation failed: {str(exc)}"}


def get_accepted_spring_2025_gpa() -> Dict[str, Any]:
    """
    Query 6: Successful Applicant Academic Profile.

    Research Question: What is the average GPA of applicants who applied for
    Spring 2025 who are Acceptances?

    Returns:
        Dict[str, Any]: Average GPA of accepted Spring 2025 applicants
    """
    try:
        # Validate inputs
        term = "Spring 2025"
        status = "Accepted"

        if not InputValidator.validate_term(term):
            return {'error': 'Invalid term format'}
        if not InputValidator.validate_status(status):
            return {'error': 'Invalid status value'}

        # Build secure query
        query = sql.SQL("""
            SELECT AVG({gpa}) as avg_gpa
            FROM {table}
            WHERE {term_field} = {term}
                AND {status_field} = {status}
                AND {gpa} IS NOT NULL
            LIMIT 1
        """).format(
            gpa=sql.Identifier('gpa'),
            table=sql.Identifier('applicants'),
            term_field=sql.Identifier('term'),
            status_field=sql.Identifier('status'),
            term=sql.Literal(term),
            status=sql.Literal(status)
        )

        # Execute query
        executor = SecureQueryExecutor()
        result = executor.execute_single_result_query(query)

        if result and result[0] is not None:
            avg_gpa = round(float(result[0]), 3)

            logger.info("Accepted Spring 2025 GPA: %s", avg_gpa)

            return {
                'question': 'What is the average GPA of applicants who applied for Spring 2025 who are Acceptances?',
                'answer': avg_gpa,
                'query': 'SELECT AVG(gpa) FROM applicants WHERE term = %s AND status = %s AND gpa IS NOT NULL LIMIT 1',
                'explanation': 'Calculates mean GPA for successful Spring 2025 applicants only',
                'methodology': 'Double-filtered AVG aggregation with term and status constraints plus LIMIT protection'
            }
        else:
            return {
                'question': 'What is the average GPA of applicants who applied for Spring 2025 who are Acceptances?',
                'answer': 0,
                'query': 'SELECT AVG(gpa) FROM applicants WHERE term = %s AND status = %s AND gpa IS NOT NULL LIMIT 1',
                'explanation': 'No accepted Spring 2025 applicants with GPA data found'
            }
    except Exception as exc:
        logger.error("Error in accepted Spring 2025 GPA query: %s", exc)
        return {'error': f"Accepted GPA calculation failed: {str(exc)}"}


def get_jhu_cs_masters_count() -> Dict[str, Any]:
    """
    Query 7: Johns Hopkins Computer Science Masters Applications.

    Research Question: How many entries are from applicants who applied to
    JHU for a masters degree in Computer Science?

    Returns:
        Dict[str, Any]: Count of JHU CS masters applications
    """
    try:
        # Sanitize input patterns
        university_pattern = "%Johns Hopkins University%"
        program_pattern = "%Computer Science%"

        # Build secure query
        query = sql.SQL("""
            SELECT COUNT(*) as count
            FROM {table}
            WHERE {program_field} LIKE {university_pattern}
                AND {program_field} LIKE {program_pattern}
                AND ({degree_field} = {ms1} OR {degree_field} = {ms2})
            LIMIT 1000
        """).format(
            table=sql.Identifier('applicants'),
            program_field=sql.Identifier('program'),
            degree_field=sql.Identifier('degree'),
            university_pattern=sql.Literal(university_pattern),
            program_pattern=sql.Literal(program_pattern),
            ms1=sql.Literal('MS'),
            ms2=sql.Literal('Master')
        )

        # Execute query
        executor = SecureQueryExecutor()
        result = executor.execute_single_result_query(query)

        count = result[0] if result else 0
        logger.info("JHU CS masters count: %s", count)

        return {
            'question': 'How many entries are from applicants who applied to JHU for a masters degree in Computer Science?',
            'answer': count,
            'query': 'SELECT COUNT(*) FROM applicants WHERE program LIKE %s AND program LIKE %s AND (degree = %s OR degree = %s) LIMIT 1000',
            'explanation': 'Count of Johns Hopkins University Computer Science masters applications',
            'methodology': 'Secure pattern matching with input sanitization and LIMIT protection'
        }
    except Exception as exc:
        logger.error("Error in JHU CS masters count query: %s", exc)
        return {'error': f"JHU count calculation failed: {str(exc)}"}


def get_all_analysis_results() -> Dict[str, Any]:
    """
    Compile all analysis results with comprehensive error handling.

    Returns:
        Dict[str, Any]: Complete analysis results or error information
    """
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
                'database_type': 'PostgreSQL (Secure)',
                'security_features': ['SQL injection protection', 'Input validation', 'Query limits'],
                'author': 'Abdullateef Mumin'
            }
        }
    except Exception as exc:
        logger.error("Error compiling results: %s", exc)
        return {'error': str(exc)}
