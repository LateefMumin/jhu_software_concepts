#!/usr/bin/env python3
"""
Secure Database Data Loading Module.

This module handles loading graduate school application data into PostgreSQL
with comprehensive security measures and input validation.

Author: Abdullateef Mumin
"""

import os
import csv
import json
import logging
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from faker import Faker
import random
import psycopg2
from psycopg2 import sql
from app import app, db
from models import Applicant
from security_utils import InputValidator

# Configure logging for data loading operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Faker for realistic data generation
fake = Faker()


def generate_realistic_applicant_data(count: int = 10000) -> List[Dict[str, Any]]:
    """
    Generate realistic graduate school applicant data for analysis.
    
    Args:
        count: Number of applicant records to generate
        
    Returns:
        List[Dict[str, Any]]: Generated applicant data dictionaries
    """
    logger.info("Generating %s realistic applicant records...", count)
    
    # Define realistic data distributions
    universities = [
        "Stanford University - Computer Science",
        "MIT - Computer Science", 
        "Johns Hopkins University - Computer Science",
        "Carnegie Mellon University - Computer Science",
        "University of California, Berkeley - Computer Science",
        "Georgia Institute of Technology - Computer Science",
        "University of Washington - Computer Science",
        "Princeton University - Computer Science",
        "Harvard University - Computer Science",
        "Yale University - Computer Science"
    ]
    
    degree_types = ["MS", "PhD", "Master", "Masters", "M.S.", "Ph.D."]
    statuses = ["Accepted", "Rejected", "Waitlisted", "Pending"]
    status_weights = [0.25, 0.55, 0.15, 0.05]
    nationalities = ["American", "International", "Other"]
    nationality_weights = [0.60, 0.35, 0.05]
    
    comments_templates = [
        "Excited about the research opportunities in this program",
        "Strong faculty match for my research interests",
        "Excellent program reputation and alumni network",
        "Great location and campus facilities",
        "Competitive funding package offered"
    ]
    
    applicants = []
    
    for i in range(count):
        # Generate realistic academic scores with proper distributions
        gpa = round(random.normalvariate(3.6, 0.4), 2)
        gpa = max(2.0, min(4.0, gpa))  # Clamp to valid range
        
        gre_quant = int(random.normalvariate(162, 8))
        gre_quant = max(130, min(170, gre_quant))
        
        gre_verbal = int(random.normalvariate(155, 7))
        gre_verbal = max(130, min(170, gre_verbal))
        
        gre_writing = round(random.normalvariate(4.2, 0.8), 1)
        gre_writing = max(0.0, min(6.0, gre_writing))
        
        # Select weighted random values
        status = random.choices(statuses, weights=status_weights)[0]
        nationality = random.choices(nationalities, weights=nationality_weights)[0]
        
        # Validate generated data
        program = InputValidator.sanitize_string(random.choice(universities))
        comments = InputValidator.sanitize_string(random.choice(comments_templates))
        
        applicant = {
            'p_id': i + 1,
            'program': program,
            'comments': comments,
            'date_added': fake.date_between(start_date='-6m', end_date='today'),
            'url': f"https://www.gradcafe.com/survey/{random.randint(10000, 99999)}",
            'status': status,
            'term': 'Spring 2025',
            'us_or_international': nationality,
            'gpa': InputValidator.validate_numeric(gpa, 0.0, 4.0),
            'gre': InputValidator.validate_numeric(gre_quant, 130, 170),
            'gre_v': InputValidator.validate_numeric(gre_verbal, 130, 170),
            'gre_aw': InputValidator.validate_numeric(gre_writing, 0.0, 6.0),
            'degree': random.choice(degree_types)
        }
        
        applicants.append(applicant)
    
    logger.info("Generated %s realistic applicant records", len(applicants))
    return applicants


def load_data_from_csv(csv_file_path: str) -> List[Dict[str, Any]]:
    """
    Load applicant data from CSV file with comprehensive validation.
    
    Args:
        csv_file_path: Path to the CSV data file
        
    Returns:
        List[Dict[str, Any]]: Parsed applicant data or empty list if file not found
    """
    if not os.path.exists(csv_file_path):
        logger.warning("CSV file not found: %s", csv_file_path)
        return []
    
    data = []
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, 1):
                try:
                    # Parse date with multiple format support
                    date_added = None
                    if row.get('date_added'):
                        try:
                            date_added = datetime.strptime(row['date_added'], '%Y-%m-%d').date()
                        except ValueError:
                            try:
                                date_added = datetime.strptime(row['date_added'], '%m/%d/%Y').date()
                            except ValueError:
                                date_added = date(2024, 3, 15)
                    
                    # Sanitize and validate all input fields
                    applicant_data = {
                        'p_id': InputValidator.validate_numeric(row.get('p_id', row_num), 1),
                        'program': InputValidator.sanitize_string(row.get('program', '')),
                        'comments': InputValidator.sanitize_string(row.get('comments', '')),
                        'date_added': date_added,
                        'url': InputValidator.sanitize_string(row.get('url', '')),
                        'status': InputValidator.sanitize_string(row.get('status', '')),
                        'term': InputValidator.sanitize_string(row.get('term', 'Spring 2025')),
                        'us_or_international': InputValidator.sanitize_string(
                            row.get('us_or_international', '')
                        ),
                        'gpa': InputValidator.validate_numeric(row.get('gpa'), 0.0, 4.0),
                        'gre': InputValidator.validate_numeric(row.get('gre'), 130, 170),
                        'gre_v': InputValidator.validate_numeric(row.get('gre_v'), 130, 170),
                        'gre_aw': InputValidator.validate_numeric(row.get('gre_aw'), 0.0, 6.0),
                        'degree': InputValidator.sanitize_string(row.get('degree', ''))
                    }
                    
                    data.append(applicant_data)
                    
                except Exception as exc:
                    logger.warning("Error parsing CSV row %s: %s", row_num, str(exc))
                    continue
        
        logger.info("Successfully loaded %s records from CSV file", len(data))
        return data
        
    except Exception as exc:
        logger.error("Error reading CSV file: %s", str(exc))
        return []


def insert_data_to_database(data: List[Dict[str, Any]]) -> None:
    """
    Insert applicant data into PostgreSQL database using secure methods.
    
    Args:
        data: List of applicant data dictionaries
        
    Raises:
        Exception: If database insertion fails
    """
    try:
        with app.app_context():
            # Clear existing data for fresh analysis
            logger.info("Clearing existing applicant data...")
            db.session.query(Applicant).delete()
            
            # Insert new data in batches for efficiency
            batch_size = 100
            total_inserted = 0
            
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                
                for record in batch:
                    try:
                        # Validate record before insertion
                        if not record.get('term') or not InputValidator.validate_term(record['term']):
                            record['term'] = 'Spring 2025'
                        
                        if record.get('status') and not InputValidator.validate_status(record['status']):
                            record['status'] = 'Pending'
                        
                        if (record.get('us_or_international') and 
                            not InputValidator.validate_nationality(record['us_or_international'])):
                            record['us_or_international'] = 'Other'
                        
                        applicant = Applicant(
                            p_id=record.get('p_id'),
                            program=record.get('program'),
                            comments=record.get('comments'),
                            date_added=record.get('date_added'),
                            url=record.get('url'),
                            status=record.get('status'),
                            term=record.get('term'),
                            us_or_international=record.get('us_or_international'),
                            gpa=record.get('gpa'),
                            gre=record.get('gre'),
                            gre_v=record.get('gre_v'),
                            gre_aw=record.get('gre_aw'),
                            degree=record.get('degree')
                        )
                        db.session.add(applicant)
                        total_inserted += 1
                        
                    except Exception as exc:
                        logger.warning("Error creating applicant record: %s", str(exc))
                        continue
                
                # Commit batch
                try:
                    db.session.commit()
                    logger.info("Inserted batch %s: %s records", i//batch_size + 1, len(batch))
                except Exception as exc:
                    db.session.rollback()
                    logger.error("Error committing batch %s: %s", i//batch_size + 1, str(exc))
                    raise
            
            logger.info("Successfully inserted %s applicant records into database", total_inserted)
            
    except Exception as exc:
        if 'db' in locals():
            db.session.rollback()
        logger.error("Error inserting data into database: %s", str(exc))
        raise


def load_sample_data() -> None:
    """Load sample data for testing and demonstration."""
    try:
        logger.info("Loading sample data for testing...")
        sample_data = generate_realistic_applicant_data(10000)
        insert_data_to_database(sample_data)
        logger.info("Sample data loaded successfully")
    except Exception as exc:
        logger.error("Error loading sample data: %s", str(exc))
        raise


if __name__ == '__main__':
    load_sample_data()
