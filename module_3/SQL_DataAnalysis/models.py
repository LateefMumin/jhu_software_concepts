#!/usr/bin/env python3
"""
Database Schema Definition

Defines the database model for graduate school applicant data.
Uses SQLAlchemy ORM for clean database abstraction and type safety 
across PostgreSQL and SQLite.

Author: Abdullateef Mumin

The Applicant model captures all relevant information from grad cafe entries
including academic metrics, demographics, and admission outcomes for comprehensive
statistical analysis of Spring 2025 graduate school applications.
"""
from app import db
from sqlalchemy import Integer, Text, Date, Float
from datetime import date

class Applicant(db.Model):
    """
    Database model for graduate school applicant data
    
    This model represents individual graduate school application entries
    scraped from grad cafe, containing academic qualifications, demographics,
    and admission outcomes. The schema follows the exact specifications
    provided in the Module 3 assignment requirements.
    """
    __tablename__ = 'applicants'
    
    # Primary key and identification
    p_id = db.Column(Integer, primary_key=True, autoincrement=True)
    
    # Program and institutional information
    program = db.Column(Text, nullable=True, comment="University and Department")
    comments = db.Column(Text, nullable=True, comment="Applicant comments and notes")
    date_added = db.Column(Date, nullable=True, comment="Date entry was added to grad cafe")
    url = db.Column(Text, nullable=True, comment="Link to original grad cafe post")
    
    # Admission outcome data
    status = db.Column(Text, nullable=True, comment="Admission decision (Accepted, Rejected, Waitlisted)")
    term = db.Column(Text, nullable=True, comment="Application term (Spring 2025, Fall 2025, etc.)")
    
    # Demographic information
    us_or_international = db.Column(Text, nullable=True, comment="Student nationality classification")
    
    # Academic performance metrics
    gpa = db.Column(Float, nullable=True, comment="Undergraduate GPA (0.0-4.0 scale)")
    gre = db.Column(Float, nullable=True, comment="GRE Quantitative score")
    gre_v = db.Column(Float, nullable=True, comment="GRE Verbal score")
    gre_aw = db.Column(Float, nullable=True, comment="GRE Analytical Writing score")
    
    # Program type
    degree = db.Column(Text, nullable=True, comment="Degree type (PhD, MS, MA, etc.)")

    def __repr__(self):
        """String representation of Applicant object"""
        return f'<Applicant {self.p_id}: {self.program} - {self.status}>'

    def to_dict(self):
        """
        Convert applicant model to dictionary for JSON serialization
        
        Returns:
            dict: Complete applicant data in dictionary format
        """
        return {
            'p_id': self.p_id,
            'program': self.program,
            'comments': self.comments,
            'date_added': self.date_added.isoformat() if self.date_added else None,
            'url': self.url,
            'status': self.status,
            'term': self.term,
            'us_or_international': self.us_or_international,
            'gpa': self.gpa,
            'gre': self.gre,
            'gre_v': self.gre_v,
            'gre_aw': self.gre_aw,
            'degree': self.degree
        }
    
    @classmethod
    def get_statistics_summary(cls):
        """
        Get basic statistics about the applicant dataset
        
        Returns:
            dict: Summary statistics for the dataset
        """
        total_count = cls.query.count()
        spring_2025_count = cls.query.filter_by(term='Spring 2025').count()
        accepted_count = cls.query.filter_by(status='Accepted').count()
        
        return {
            'total_applicants': total_count,
            'spring_2025_applicants': spring_2025_count,
            'total_accepted': accepted_count,
            'acceptance_rate': round((accepted_count / total_count * 100), 2) if total_count > 0 else 0
        }
    
    @classmethod
    def create_sample_record(cls, **kwargs):
        """
        Create a sample applicant record with default values
        
        Args:
            **kwargs: Override values for specific fields
            
        Returns:
            Applicant: New applicant instance
        """
        defaults = {
            'program': 'Sample University - Computer Science',
            'comments': 'Graduate program application',
            'date_added': date.today(),
            'status': 'Pending',
            'term': 'Spring 2025',
            'us_or_international': 'American',
            'gpa': 3.5,
            'gre': 160,
            'gre_v': 155,
            'gre_aw': 4.0,
            'degree': 'MS'
        }
        
        # Update defaults with provided kwargs
        defaults.update(kwargs)
        
        return cls(**defaults)