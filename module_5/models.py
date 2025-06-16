#!/usr/bin/env python3
"""
Database Schema Definition.

Defines the database model for graduate school applicant data using
SQLAlchemy ORM with proper type safety and validation.

Author: Abdullateef Mumin
"""

from datetime import date
from typing import Dict, Any, Optional
from sqlalchemy import Integer, Text, Date, Float
from app import db


class Applicant(db.Model):
    """
    Database model for graduate school applicant data.
    
    This model represents individual graduate school application entries
    with academic qualifications, demographics, and admission outcomes.
    """
    
    __tablename__ = 'applicants'
    
    # Primary key and identification
    p_id = db.Column(Integer, primary_key=True, autoincrement=True)
    
    # Program and institutional information
    program = db.Column(Text, nullable=True, comment="University and Department")
    comments = db.Column(Text, nullable=True, comment="Applicant comments and notes")
    date_added = db.Column(Date, nullable=True, comment="Date entry was added")
    url = db.Column(Text, nullable=True, comment="Link to original post")
    
    # Admission outcome data
    status = db.Column(Text, nullable=True, comment="Admission decision")
    term = db.Column(Text, nullable=True, comment="Application term")
    
    # Demographic information
    us_or_international = db.Column(Text, nullable=True, comment="Nationality classification")
    
    # Academic performance metrics
    gpa = db.Column(Float, nullable=True, comment="Undergraduate GPA (0.0-4.0 scale)")
    gre = db.Column(Float, nullable=True, comment="GRE Quantitative score")
    gre_v = db.Column(Float, nullable=True, comment="GRE Verbal score")
    gre_aw = db.Column(Float, nullable=True, comment="GRE Analytical Writing score")
    
    # Program type
    degree = db.Column(Text, nullable=True, comment="Degree type")

    def __repr__(self) -> str:
        """String representation of Applicant object."""
        return f'<Applicant {self.p_id}: {self.program} - {self.status}>'

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert applicant model to dictionary for JSON serialization.
        
        Returns:
            Dict[str, Any]: Complete applicant data in dictionary format
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
    def get_statistics_summary(cls) -> Dict[str, Any]:
        """
        Get basic statistics about the applicant dataset.
        
        Returns:
            Dict[str, Any]: Summary statistics for the dataset
        """
        total_count = cls.query.count()
        spring_2025_count = cls.query.filter_by(term='Spring 2025').count()
        accepted_count = cls.query.filter_by(status='Accepted').count()
        
        acceptance_rate = 0
        if total_count > 0:
            acceptance_rate = round((accepted_count / total_count * 100), 2)
        
        return {
            'total_applicants': total_count,
            'spring_2025_applicants': spring_2025_count,
            'total_accepted': accepted_count,
            'acceptance_rate': acceptance_rate
        }
    
    @classmethod
    def create_sample_record(cls, **kwargs) -> 'Applicant':
        """
        Create a sample applicant record with default values.
        
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
