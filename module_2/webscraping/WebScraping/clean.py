"""
Data Cleaning Module for GradCafe Applicant Data
Handles data processing, validation, and formatting
"""

import json
import re
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GradCafeDataCleaner:
    def __init__(self):
        self.cleaned_data = []
        self.cleaning_stats = {
            'total_entries': 0,
            'cleaned_entries': 0,
            'removed_entries': 0,
            'fields_cleaned': {}
        }
    
    def _clean_text(self, text: str) -> str:
        """Remove HTML tags, extra whitespace, and normalize text"""
        if not text or text.strip() == "":
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', str(text))
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters that might be artifacts
        text = re.sub(r'[^\w\s\-.,;:()&/]', '', text)
        
        return text
    
    def _standardize_decision_status(self, status: str) -> str:
        """Standardize decision status values"""
        if not status:
            return ""
        
        status = status.lower().strip()
        
        if any(word in status for word in ['accept', 'admit']):
            return "Accepted"
        elif any(word in status for word in ['reject', 'den']):
            return "Rejected"
        elif any(word in status for word in ['wait', 'list']):
            return "Waitlisted"
        elif any(word in status for word in ['interview']):
            return "Interview"
        else:
            return status.title()
    
    def _clean_date(self, date_str: str) -> str:
        """Clean and standardize date formats"""
        if not date_str:
            return ""
        
        date_str = self._clean_text(date_str)
        
        # Common date patterns
        date_patterns = [
            r'(\d{1,2})\s+(\w{3})\s+(\d{4})',  # 15 Jan 2024
            r'(\w{3})\s+(\d{1,2}),?\s+(\d{4})',  # Jan 15, 2024
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # 1/15/2024
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # 2024-01-15
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_str)
            if match:
                try:
                    # Try to parse and reformat to standard format
                    if pattern == date_patterns[0]:  # 15 Jan 2024
                        day, month, year = match.groups()
                        return f"{day} {month} {year}"
                    elif pattern == date_patterns[1]:  # Jan 15, 2024
                        month, day, year = match.groups()
                        return f"{day} {month} {year}"
                    elif pattern == date_patterns[2]:  # 1/15/2024
                        month, day, year = match.groups()
                        return f"{day.zfill(2)}/{month.zfill(2)}/{year}"
                    elif pattern == date_patterns[3]:  # 2024-01-15
                        year, month, day = match.groups()
                        return f"{day}/{month}/{year}"
                except:
                    continue
        
        return date_str  # Return as-is if no pattern matches
    
    def _clean_gpa(self, gpa_str: str) -> str:
        """Clean and validate GPA values"""
        if not gpa_str:
            return ""
        
        gpa_str = self._clean_text(gpa_str)
        
        # Extract numeric GPA value
        gpa_match = re.search(r'(\d+\.?\d*)', gpa_str)
        if gpa_match:
            try:
                gpa_value = float(gpa_match.group(1))
                if 0.0 <= gpa_value <= 4.0:
                    return f"{gpa_value:.2f}"
                elif gpa_value > 4.0 and gpa_value <= 10.0:
                    # Might be on a 10-point scale, convert to 4.0 scale
                    converted = (gpa_value / 10.0) * 4.0
                    return f"{converted:.2f}"
            except ValueError:
                pass
        
        return ""
    
    def _clean_gre_score(self, score_str: str) -> str:
        """Clean and validate GRE scores"""
        if not score_str:
            return ""
        
        score_str = self._clean_text(score_str)
        
        # Extract numeric score
        score_match = re.search(r'(\d+)', score_str)
        if score_match:
            try:
                score = int(score_match.group(1))
                # Validate GRE score ranges
                if 130 <= score <= 170:  # Valid GRE V/Q range
                    return str(score)
                elif 200 <= score <= 800:  # Old GRE scale
                    return str(score)
            except ValueError:
                pass
        
        return ""
    
    def _clean_gre_aw(self, aw_str: str) -> str:
        """Clean and validate GRE Analytical Writing scores"""
        if not aw_str:
            return ""
        
        aw_str = self._clean_text(aw_str)
        
        # Extract AW score (usually 0.0 to 6.0)
        aw_match = re.search(r'(\d+\.?\d*)', aw_str)
        if aw_match:
            try:
                aw_score = float(aw_match.group(1))
                if 0.0 <= aw_score <= 6.0:
                    return f"{aw_score:.1f}"
            except ValueError:
                pass
        
        return ""
    
    def _clean_degree_type(self, degree_str: str) -> str:
        """Standardize degree type values"""
        if not degree_str:
            return ""
        
        degree_str = self._clean_text(degree_str).lower()
        
        if any(word in degree_str for word in ['phd', 'ph.d', 'doctorate', 'doctoral']):
            return "PhD"
        elif any(word in degree_str for word in ['masters', 'master', 'ms', 'm.s', 'ma', 'm.a']):
            return "Masters"
        elif any(word in degree_str for word in ['bachelor', 'undergrad', 'bs', 'ba']):
            return "Bachelors"
        else:
            return degree_str.title()
    
    def _clean_semester_year(self, semester_year_str: str) -> Dict[str, str]:
        """Extract and clean semester and year information"""
        if not semester_year_str:
            return {"semester": "", "year": ""}
        
        semester_year_str = self._clean_text(semester_year_str).lower()
        
        # Extract year
        year_match = re.search(r'(20\d{2})', semester_year_str)
        year = year_match.group(1) if year_match else ""
        
        # Extract semester
        semester = ""
        if any(word in semester_year_str for word in ['fall', 'autumn']):
            semester = "Fall"
        elif any(word in semester_year_str for word in ['spring']):
            semester = "Spring"
        elif any(word in semester_year_str for word in ['summer']):
            semester = "Summer"
        elif any(word in semester_year_str for word in ['winter']):
            semester = "Winter"
        
        return {"semester": semester, "year": year}
    
    def _validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate if an entry has sufficient data to be useful"""
        required_fields = ['university', 'program_name']
        
        for field in required_fields:
            if not entry.get(field) or entry[field].strip() == "":
                return False
        
        return True
    
    def clean_entry(self, entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Clean a single entry"""
        try:
            cleaned_entry = {}
            
            # Clean basic text fields
            cleaned_entry['program_name'] = self._clean_text(entry.get('program_name', ''))
            cleaned_entry['university'] = self._clean_text(entry.get('university', ''))
            cleaned_entry['comments'] = self._clean_text(entry.get('comments', ''))
            cleaned_entry['url'] = entry.get('url', '')
            
            # Clean and standardize decision status
            cleaned_entry['applicant_status'] = self._standardize_decision_status(
                entry.get('applicant_status', '')
            )
            
            # Clean dates
            cleaned_entry['date_added'] = self._clean_date(entry.get('date_added', ''))
            cleaned_entry['acceptance_date'] = self._clean_date(entry.get('acceptance_date', ''))
            cleaned_entry['rejection_date'] = self._clean_date(entry.get('rejection_date', ''))
            
            # Clean semester and year
            semester_year_info = self._clean_semester_year(entry.get('semester_year', ''))
            cleaned_entry['semester'] = semester_year_info['semester']
            cleaned_entry['year'] = semester_year_info['year']
            
            # Clean international status
            intl_status = self._clean_text(entry.get('international_american', ''))
            if intl_status.lower() in ['international', 'foreign']:
                cleaned_entry['international_american'] = 'International'
            elif intl_status.lower() in ['domestic', 'american', 'usa', 'us']:
                cleaned_entry['international_american'] = 'American'
            else:
                cleaned_entry['international_american'] = ''
            
            # Clean GPA
            cleaned_entry['gpa'] = self._clean_gpa(entry.get('gpa', ''))
            
            # Clean GRE scores
            cleaned_entry['gre_verbal'] = self._clean_gre_score(entry.get('gre_verbal', ''))
            cleaned_entry['gre_quantitative'] = self._clean_gre_score(
                entry.get('gre_score', '').split('Q:')[-1].split(',')[0] if 'Q:' in entry.get('gre_score', '') else ''
            )
            cleaned_entry['gre_aw'] = self._clean_gre_aw(entry.get('gre_aw', ''))
            
            # Clean degree type
            cleaned_entry['degree_type'] = self._clean_degree_type(entry.get('degree_type', ''))
            
            # Validate entry
            if not self._validate_entry(cleaned_entry):
                return None
            
            return cleaned_entry
            
        except Exception as e:
            logger.error(f"Error cleaning entry: {e}")
            return None
    
    def clean_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean all entries in the dataset"""
        logger.info(f"Starting data cleaning for {len(raw_data)} entries...")
        
        self.cleaning_stats['total_entries'] = len(raw_data)
        self.cleaned_data = []
        
        for i, entry in enumerate(raw_data):
            cleaned_entry = self.clean_entry(entry)
            
            if cleaned_entry:
                self.cleaned_data.append(cleaned_entry)
                self.cleaning_stats['cleaned_entries'] += 1
            else:
                self.cleaning_stats['removed_entries'] += 1
            
            if (i + 1) % 1000 == 0:
                logger.info(f"Processed {i + 1} entries...")
        
        logger.info(f"Data cleaning completed:")
        logger.info(f"  Total entries: {self.cleaning_stats['total_entries']}")
        logger.info(f"  Cleaned entries: {self.cleaning_stats['cleaned_entries']}")
        logger.info(f"  Removed entries: {self.cleaning_stats['removed_entries']}")
        
        return self.cleaned_data
    
    def save_cleaned_data(self, filename='applicant_data.json'):
        """Save cleaned data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.cleaned_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Cleaned data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving cleaned data: {e}")
    
    def load_data(self, filename='applicant_data.json') -> List[Dict[str, Any]]:
        """Load cleaned data from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data)} entries from {filename}")
            return data
        except Exception as e:
            logger.error(f"Error loading data from {filename}: {e}")
            return []
    
    def get_cleaning_stats(self) -> Dict[str, Any]:
        """Return cleaning statistics"""
        return self.cleaning_stats

def main():
    """Main function for testing the cleaner"""
    cleaner = GradCafeDataCleaner()
    
    # Test with sample data
    sample_data = [
        {
            'program_name': 'Computer Science',
            'university': 'Stanford University',
            'applicant_status': 'accepted',
            'gpa': '3.75',
            'gre_verbal': '165',
            'date_added': '15 Jan 2024'
        }
    ]
    
    cleaned = cleaner.clean_data(sample_data)
    print(f"Cleaned {len(cleaned)} entries")
    
    if cleaned:
        print("Sample cleaned entry:")
        print(json.dumps(cleaned[0], indent=2))

if __name__ == "__main__":
    main()
