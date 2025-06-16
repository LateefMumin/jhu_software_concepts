#!/usr/bin/env python3
"""
Security utilities for SQL injection prevention and input validation.

This module provides secure database query composition using psycopg's
sql module and comprehensive input validation functions.

Author: Abdullateef Mumin
"""

import re
import logging
from typing import Any, Dict, List, Optional, Union
from psycopg2 import sql

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryBuilder:
    """Secure SQL query builder using psycopg's sql composition."""

    @staticmethod
    def build_count_query(table: str, conditions: Dict[str, Any]) -> sql.Composed:
        """
        Build a secure COUNT query with conditions.
        
        Args:
            table: Table name to query
            conditions: Dictionary of field:value conditions
            
        Returns:
            sql.Composed: Secure SQL query object
        """
        query = sql.SQL("SELECT COUNT(*) FROM {table}").format(
            table=sql.Identifier(table)
        )
        
        if conditions:
            where_clauses = []
            for field, value in conditions.items():
                if value is not None:
                    where_clauses.append(
                        sql.SQL("{field} = {value}").format(
                            field=sql.Identifier(field),
                            value=sql.Literal(value)
                        )
                    )
            
            if where_clauses:
                query = sql.SQL("{query} WHERE {conditions} LIMIT 1").format(
                    query=query,
                    conditions=sql.SQL(" AND ").join(where_clauses)
                )
        
        return query

    @staticmethod
    def build_average_query(table: str, fields: List[str], 
                          conditions: Dict[str, Any]) -> sql.Composed:
        """
        Build a secure AVG query for multiple fields.
        
        Args:
            table: Table name to query
            fields: List of field names to average
            conditions: Dictionary of field:value conditions
            
        Returns:
            sql.Composed: Secure SQL query object
        """
        avg_fields = []
        for field in fields:
            avg_fields.append(
                sql.SQL("AVG({field}) as avg_{field}").format(
                    field=sql.Identifier(field)
                )
            )
        
        query = sql.SQL("SELECT {fields} FROM {table}").format(
            fields=sql.SQL(", ").join(avg_fields),
            table=sql.Identifier(table)
        )
        
        # Add WHERE conditions
        if conditions:
            where_clauses = []
            for field, value in conditions.items():
                if value is not None:
                    where_clauses.append(
                        sql.SQL("{field} = {value}").format(
                            field=sql.Identifier(field),
                            value=sql.Literal(value)
                        )
                    )
            
            # Add NOT NULL conditions for averaged fields
            for field in fields:
                where_clauses.append(
                    sql.SQL("{field} IS NOT NULL").format(
                        field=sql.Identifier(field)
                    )
                )
            
            if where_clauses:
                query = sql.SQL("{query} WHERE {conditions} LIMIT 10000").format(
                    query=query,
                    conditions=sql.SQL(" AND ").join(where_clauses)
                )
        
        return query

    @staticmethod
    def build_percentage_query(table: str, condition_field: str, 
                             condition_value: str) -> sql.Composed:
        """
        Build a secure percentage calculation query.
        
        Args:
            table: Table name to query
            condition_field: Field to check for condition
            condition_value: Value to match for percentage calculation
            
        Returns:
            sql.Composed: Secure SQL query object
        """
        query = sql.SQL("""
            SELECT 
                COUNT(CASE WHEN {field} = {value} THEN 1 END) * 100.0 / COUNT(*) as percentage,
                COUNT(CASE WHEN {field} = {value} THEN 1 END) as match_count,
                COUNT(*) as total_count
            FROM {table}
            WHERE {field} IS NOT NULL
            LIMIT 1
        """).format(
            field=sql.Identifier(condition_field),
            value=sql.Literal(condition_value),
            table=sql.Identifier(table)
        )
        
        return query

    @staticmethod
    def build_like_query(table: str, field: str, pattern: str, 
                        additional_conditions: Dict[str, Any]) -> sql.Composed:
        """
        Build a secure LIKE query with pattern matching.
        
        Args:
            table: Table name to query
            field: Field to search with LIKE
            pattern: Pattern to match (will be sanitized)
            additional_conditions: Additional WHERE conditions
            
        Returns:
            sql.Composed: Secure SQL query object
        """
        # Sanitize pattern to prevent injection
        sanitized_pattern = InputValidator.sanitize_like_pattern(pattern)
        
        query = sql.SQL("SELECT COUNT(*) FROM {table}").format(
            table=sql.Identifier(table)
        )
        
        where_clauses = [
            sql.SQL("{field} LIKE {pattern}").format(
                field=sql.Identifier(field),
                pattern=sql.Literal(sanitized_pattern)
            )
        ]
        
        # Add additional conditions
        for cond_field, value in additional_conditions.items():
            if value is not None:
                where_clauses.append(
                    sql.SQL("{field} = {value}").format(
                        field=sql.Identifier(cond_field),
                        value=sql.Literal(value)
                    )
                )
        
        query = sql.SQL("{query} WHERE {conditions} LIMIT 1000").format(
            query=query,
            conditions=sql.SQL(" AND ").join(where_clauses)
        )
        
        return query


class InputValidator:
    """Input validation and sanitization utilities."""

    @staticmethod
    def sanitize_string(input_str: str, max_length: int = 255) -> str:
        """
        Sanitize string input to prevent injection attacks.
        
        Args:
            input_str: Input string to sanitize
            max_length: Maximum allowed length
            
        Returns:
            str: Sanitized string
        """
        if not isinstance(input_str, str):
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\';\\]', '', input_str)
        
        # Limit length
        sanitized = sanitized[:max_length]
        
        # Strip whitespace
        return sanitized.strip()

    @staticmethod
    def sanitize_like_pattern(pattern: str) -> str:
        """
        Sanitize LIKE pattern to prevent SQL injection.
        
        Args:
            pattern: LIKE pattern to sanitize
            
        Returns:
            str: Sanitized pattern
        """
        if not isinstance(pattern, str):
            return "%"
        
        # Escape special LIKE characters
        pattern = pattern.replace('\\', '\\\\')
        pattern = pattern.replace('%', '\\%')
        pattern = pattern.replace('_', '\\_')
        
        # Remove dangerous characters
        pattern = re.sub(r'[<>"\';]', '', pattern)
        
        # Wrap with wildcards
        return f"%{pattern}%"

    @staticmethod
    def validate_numeric(value: Any, min_val: float = None, 
                        max_val: float = None) -> Optional[float]:
        """
        Validate and convert numeric input.
        
        Args:
            value: Value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            
        Returns:
            Optional[float]: Validated numeric value or None if invalid
        """
        try:
            num_val = float(value)
            
            if min_val is not None and num_val < min_val:
                return None
            if max_val is not None and num_val > max_val:
                return None
            
            return num_val
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_term(term: str) -> bool:
        """
        Validate academic term format.
        
        Args:
            term: Academic term to validate
            
        Returns:
            bool: True if valid term format
        """
        if not isinstance(term, str):
            return False
        
        # Valid term patterns: "Spring 2025", "Fall 2024", etc.
        pattern = r'^(Spring|Fall|Summer|Winter)\s+\d{4}$'
        return bool(re.match(pattern, term))

    @staticmethod
    def validate_status(status: str) -> bool:
        """
        Validate admission status value.
        
        Args:
            status: Status to validate
            
        Returns:
            bool: True if valid status
        """
        valid_statuses = {'Accepted', 'Rejected', 'Waitlisted', 'Pending'}
        return status in valid_statuses

    @staticmethod
    def validate_nationality(nationality: str) -> bool:
        """
        Validate nationality classification.
        
        Args:
            nationality: Nationality to validate
            
        Returns:
            bool: True if valid nationality
        """
        valid_nationalities = {'American', 'International', 'Other'}
        return nationality in valid_nationalities


def log_query_execution(query: sql.Composed, params: Dict[str, Any] = None) -> None:
    """
    Log SQL query execution for security monitoring.
    
    Args:
        query: SQL query being executed
        params: Query parameters
    """
    logger.info("Executing secure SQL query: %s", query.as_string())
    if params:
        logger.debug("Query parameters: %s", params)
