"""
Main execution script for GradCafe web scraping application
Orchestrates the scraping and cleaning process
"""

import os
import json
import logging
from datetime import datetime
from scrape import GradCafeScraper
from clean import GradCafeDataCleaner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gradcafe_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GradCafeApplication:
    def __init__(self):
        self.scraper = GradCafeScraper()
        self.cleaner = GradCafeDataCleaner()
        self.target_entries = 10000
        
    def scrape_data(self):
        """Execute the scraping process"""
        logger.info("Starting data scraping process...")
        
        try:
            # Scrape data from GradCafe
            raw_data = self.scraper.scrape_data(max_entries=self.target_entries)
            
            if not raw_data:
                logger.error("No data was scraped. Aborting process.")
                return False
            
            # Save raw data
            self.scraper.save_raw_data('raw_applicant_data.json')
            
            logger.info(f"Successfully scraped {len(raw_data)} entries")
            return True
            
        except Exception as e:
            logger.error(f"Error during scraping process: {e}")
            return False
    
    def clean_data(self):
        """Execute the data cleaning process"""
        logger.info("Starting data cleaning process...")
        
        try:
            # Load raw data
            if not os.path.exists('raw_applicant_data.json'):
                logger.error("Raw data file not found. Please run scraping first.")
                return False
            
            with open('raw_applicant_data.json', 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # Clean the data
            cleaned_data = self.cleaner.clean_data(raw_data)
            
            if not cleaned_data:
                logger.error("No data remained after cleaning. Check data quality.")
                return False
            
            # Save cleaned data
            self.cleaner.save_cleaned_data('applicant_data.json')
            
            # Print cleaning statistics
            stats = self.cleaner.get_cleaning_stats()
            logger.info("Cleaning Statistics:")
            for key, value in stats.items():
                logger.info(f"  {key}: {value}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error during cleaning process: {e}")
            return False
    
    def save_data(self, data, filename='applicant_data.json'):
        """Save data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving data to {filename}: {e}")
    
    def load_data(self, filename='applicant_data.json'):
        """Load data from JSON file"""
        try:
            if not os.path.exists(filename):
                logger.error(f"File {filename} not found")
                return []
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Loaded {len(data)} entries from {filename}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading data from {filename}: {e}")
            return []
    
    def generate_summary_report(self):
        """Generate a summary report of the scraped data"""
        try:
            data = self.load_data('applicant_data.json')
            
            if not data:
                logger.warning("No data available for summary report")
                return
            
            # Basic statistics
            total_entries = len(data)
            
            # Count by status
            status_counts = {}
            for entry in data:
                status = entry.get('applicant_status', 'Unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Count by degree type
            degree_counts = {}
            for entry in data:
                degree = entry.get('degree_type', 'Unknown')
                degree_counts[degree] = degree_counts.get(degree, 0) + 1
            
            # Top universities
            university_counts = {}
            for entry in data:
                university = entry.get('university', 'Unknown')
                university_counts[university] = university_counts.get(university, 0) + 1
            
            top_universities = sorted(university_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Generate report
            report = {
                'generation_date': datetime.now().isoformat(),
                'total_entries': total_entries,
                'status_distribution': status_counts,
                'degree_type_distribution': degree_counts,
                'top_10_universities': dict(top_universities),
                'data_quality': {
                    'entries_with_gpa': sum(1 for entry in data if entry.get('gpa')),
                    'entries_with_gre': sum(1 for entry in data if entry.get('gre_verbal')),
                    'entries_with_comments': sum(1 for entry in data if entry.get('comments'))
                }
            }
            
            # Save report
            with open('data_summary_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info("Summary report generated:")
            logger.info(f"  Total entries: {total_entries}")
            logger.info(f"  Status distribution: {status_counts}")
            logger.info(f"  Degree distribution: {degree_counts}")
            
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
    
    def run_full_pipeline(self):
        """Execute the complete scraping and cleaning pipeline"""
        logger.info("Starting GradCafe data collection pipeline...")
        
        start_time = datetime.now()
        
        # Step 1: Scrape data
        if not self.scrape_data():
            logger.error("Scraping failed. Aborting pipeline.")
            return False
        
        # Step 2: Clean data
        if not self.clean_data():
            logger.error("Data cleaning failed. Aborting pipeline.")
            return False
        
        # Step 3: Generate summary report
        self.generate_summary_report()
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info(f"Pipeline completed successfully in {duration}")
        logger.info("Output files generated:")
        logger.info("  - raw_applicant_data.json (raw scraped data)")
        logger.info("  - applicant_data.json (cleaned data)")
        logger.info("  - data_summary_report.json (summary statistics)")
        logger.info("  - robots_txt_content.txt (robots.txt compliance)")
        logger.info("  - gradcafe_scraper.log (execution log)")
        
        return True

def main():
    """Main execution function"""
    print("GradCafe Web Scraper Application")
    print("================================")
    
    app = GradCafeApplication()
    
    # Check if we should run the full pipeline or individual components
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'scrape':
            app.scrape_data()
        elif command == 'clean':
            app.clean_data()
        elif command == 'report':
            app.generate_summary_report()
        elif command == 'load':
            data = app.load_data()
            print(f"Loaded {len(data)} entries")
            if data:
                print("Sample entry:")
                print(json.dumps(data[0], indent=2))
        else:
            print("Unknown command. Use: scrape, clean, report, or load")
    else:
        # Run full pipeline
        success = app.run_full_pipeline()
        
        if success:
            print("\nPipeline completed successfully!")
            print("Check the generated files for results.")
        else:
            print("\nPipeline failed. Check the log file for details.")

if __name__ == "__main__":
    main()
