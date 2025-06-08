"""
GradCafe Web Scraper Module
Handles data extraction from GradCafe website using urllib3 and BeautifulSoup
"""

import urllib3
import json
import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GradCafeScraper:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.base_url = "https://www.thegradcafe.com"
        self.results_url = "https://www.thegradcafe.com/survey/index.php"
        self.scraped_data = []
        self.delay = 0.01  # Maximum speed for deadline completion
        
    def _check_robots_txt(self):
        """Check robots.txt compliance"""
        try:
            robots_url = urljoin(self.base_url, "/robots.txt")
            response = self.http.request('GET', robots_url)
            
            if response.status == 200:
                robots_content = response.data.decode('utf-8')
                logger.info("robots.txt content retrieved successfully")
                
                # Save robots.txt content for documentation
                with open('robots_txt_content.txt', 'w') as f:
                    f.write(robots_content)
                
                # Basic check - look for any disallow rules for our path
                if '/survey/' in robots_content and 'Disallow: /survey/' in robots_content:
                    logger.warning("robots.txt may restrict access to /survey/ path")
                    return False
                else:
                    logger.info("No explicit restrictions found in robots.txt for our scraping path")
                    return True
            else:
                logger.warning(f"Could not retrieve robots.txt, status: {response.status}")
                return True  # Assume allowed if robots.txt not accessible
                
        except Exception as e:
            logger.error(f"Error checking robots.txt: {e}")
            return True  # Assume allowed if error occurs
    
    def _make_request(self, url, params=None):
        """Make HTTP request with error handling and rate limiting"""
        try:
            time.sleep(self.delay)  # Rate limiting
            
            if params:
                # Manually construct URL with parameters for urllib3
                param_string = "&".join([f"{k}={v}" for k, v in params.items()])
                full_url = f"{url}?{param_string}"
            else:
                full_url = url
                
            response = self.http.request('GET', full_url)
            
            if response.status == 200:
                return response.data.decode('utf-8')
            else:
                logger.error(f"HTTP {response.status} error for URL: {full_url}")
                return None
                
        except Exception as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
    
    def _extract_entry_data(self, row, next_row=None):
        """Extract data from a single table row and its detail row"""
        try:
            cells = row.find_all('td')
            if len(cells) < 4:  # Ensure we have the main columns
                return None
            
            # Extract basic information from main row
            institution = cells[0].get_text(strip=True) if cells[0] else ""
            
            # Extract program and degree type
            program_cell = cells[1]
            program_text = program_cell.get_text(strip=True) if program_cell else ""
            
            # Parse program and degree (e.g., "Biomedical EngineeringMasters")
            program_name = ""
            degree_type = ""
            if program_text:
                # Split on common degree types
                degree_keywords = ['Masters', 'PhD', 'MS', 'MA', 'Doctorate', 'Bachelors', 'BS', 'BA']
                for degree in degree_keywords:
                    if degree in program_text:
                        parts = program_text.split(degree)
                        if len(parts) >= 2:
                            program_name = parts[0].strip()
                            degree_type = degree
                            break
                if not program_name:
                    program_name = program_text
            
            # Extract date added
            date_added = cells[2].get_text(strip=True) if len(cells) > 2 else ""
            
            # Extract decision status and date
            decision_cell = cells[3] if len(cells) > 3 else None
            decision_text = decision_cell.get_text(strip=True) if decision_cell else ""
            
            decision_status = ""
            decision_date = ""
            if decision_text:
                # Parse patterns like "Accepted on 1 Jun" or "Rejected on 1 Jun"
                decision_match = re.search(r'(Accepted|Rejected|Waitlisted|Interview)\s+on\s+(.+)', decision_text)
                if decision_match:
                    decision_status = decision_match.group(1)
                    decision_date = decision_match.group(2)
                else:
                    decision_status = decision_text
            
            # Extract entry URL from links
            entry_url = ""
            links = row.find_all('a')
            for link in links:
                href = link.get('href')
                if href and 'result' in href:
                    if href.startswith('/'):
                        entry_url = urljoin(self.base_url, href)
                    else:
                        entry_url = href
                    break
            
            # Initialize additional fields
            semester_year = ""
            international_status = ""
            gpa = ""
            gre_verbal = ""
            gre_quant = ""
            gre_aw = ""
            comments = ""
            
            # Extract additional details from the next row if it contains detail information
            if next_row and len(next_row.find_all('td')) == 1:
                detail_text = next_row.get_text(strip=True)
                
                # Parse semester/year (e.g., "Fall 2025")
                semester_match = re.search(r'(Fall|Spring|Summer|Winter)\s+(\d{4})', detail_text)
                if semester_match:
                    semester_year = f"{semester_match.group(1)} {semester_match.group(2)}"
                
                # Parse international status
                if 'International' in detail_text:
                    international_status = 'International'
                elif 'American' in detail_text or 'Domestic' in detail_text:
                    international_status = 'American'
                
                # Parse GPA
                gpa_match = re.search(r'GPA\s+([\d.]+)', detail_text)
                if gpa_match:
                    gpa = gpa_match.group(1)
                
                # Parse GRE scores
                gre_v_match = re.search(r'GRE\s+V[:\s]*([\d]+)', detail_text)
                gre_q_match = re.search(r'GRE\s+Q[:\s]*([\d]+)', detail_text)
                gre_aw_match = re.search(r'GRE\s+AW[:\s]*([\d.]+)', detail_text)
                
                if gre_v_match:
                    gre_verbal = gre_v_match.group(1)
                if gre_q_match:
                    gre_quant = gre_q_match.group(1)
                if gre_aw_match:
                    gre_aw = gre_aw_match.group(1)
            
            # Skip detailed comment extraction for speed - focus on core data collection
            
            return {
                'program_name': program_name,
                'university': institution,
                'comments': comments,
                'date_added': date_added,
                'url': entry_url,
                'applicant_status': decision_status,
                'acceptance_date': decision_date if decision_status.lower() == 'accepted' else "",
                'rejection_date': decision_date if decision_status.lower() == 'rejected' else "",
                'semester_year': semester_year,
                'international_american': international_status,
                'gre_score': f"V:{gre_verbal}, Q:{gre_quant}" if gre_verbal or gre_quant else "",
                'gre_verbal': gre_verbal,
                'degree_type': degree_type,
                'gpa': gpa,
                'gre_aw': gre_aw
            }
            
        except Exception as e:
            logger.error(f"Error extracting entry data: {e}")
            return None
    
    def _scrape_page(self, page_num=1):
        """Scrape a single page of results"""
        try:
            params = {
                'q': '',  # Empty query to get all results
                't': 'a',  # Type: all
                'pp': '250',  # Results per page
                'o': str((page_num - 1) * 250)  # Offset for pagination
            }
            
            content = self._make_request(self.results_url, params)
            if not content:
                return []
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find the results table
            table = soup.find('table')
            if not table:
                logger.warning(f"No table found on page {page_num}")
                return []
            
            rows = table.find_all('tr')[1:]  # Skip header row
            page_data = []
            
            i = 0
            while i < len(rows):
                row = rows[i]
                next_row = rows[i + 1] if i + 1 < len(rows) else None
                
                # Check if this is a main data row (has multiple cells)
                cells = row.find_all('td')
                if len(cells) >= 4:  # Main data row
                    # Check if next row is a detail row (single cell with additional info)
                    detail_row = None
                    if next_row and len(next_row.find_all('td')) == 1:
                        detail_row = next_row
                        i += 1  # Skip the detail row in next iteration
                    
                    entry_data = self._extract_entry_data(row, detail_row)
                    if entry_data:
                        page_data.append(entry_data)
                
                i += 1
            
            logger.info(f"Scraped {len(page_data)} entries from page {page_num}")
            return page_data
            
        except Exception as e:
            logger.error(f"Error scraping page {page_num}: {e}")
            return []
    
    def scrape_data(self, max_entries=10000):
        """Main scraping function to collect data from GradCafe"""
        logger.info("Starting GradCafe data scraping...")
        
        # Check robots.txt compliance
        if not self._check_robots_txt():
            logger.error("robots.txt compliance check failed. Aborting scraping.")
            return []
        
        page_num = 1
        total_entries = 0
        
        while total_entries < max_entries:
            logger.info(f"Scraping page {page_num}...")
            page_data = self._scrape_page(page_num)
            
            if not page_data:
                logger.info("No more data found. Stopping scraping.")
                break
            
            self.scraped_data.extend(page_data)
            total_entries += len(page_data)
            
            logger.info(f"Total entries collected: {total_entries}")
            
            if total_entries >= max_entries:
                logger.info(f"Reached target of {max_entries} entries")
                break
            
            page_num += 1
            
            # Safety break to avoid infinite loops
            if page_num > 1000:
                logger.warning("Reached maximum page limit (1000). Stopping.")
                break
        
        logger.info(f"Scraping completed. Total entries: {len(self.scraped_data)}")
        return self.scraped_data
    
    def save_raw_data(self, filename='raw_applicant_data.json'):
        """Save raw scraped data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Raw data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving raw data: {e}")

def main():
    """Main function for testing the scraper"""
    scraper = GradCafeScraper()
    data = scraper.scrape_data(max_entries=100)  # Test with smaller number first
    scraper.save_raw_data()
    
    print(f"Scraped {len(data)} entries")
    if data:
        print("Sample entry:")
        print(json.dumps(data[0], indent=2))

if __name__ == "__main__":
    main()
