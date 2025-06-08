"""
Robots.txt Compliance Checker
Validates that scraping activities comply with robots.txt rules
"""

import urllib3
import re
import logging
from urllib.parse import urljoin, urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RobotsChecker:
    def __init__(self, base_url="https://www.thegradcafe.com"):
        self.base_url = base_url
        self.http = urllib3.PoolManager()
        self.robots_content = None
        self.rules = {}
        
    def fetch_robots_txt(self):
        """Fetch and parse robots.txt file"""
        try:
            robots_url = urljoin(self.base_url, "/robots.txt")
            logger.info(f"Fetching robots.txt from: {robots_url}")
            
            response = self.http.request('GET', robots_url)
            
            if response.status == 200:
                self.robots_content = response.data.decode('utf-8')
                logger.info("Successfully retrieved robots.txt")
                
                # Save robots.txt content for documentation
                with open('robots_txt_content.txt', 'w', encoding='utf-8') as f:
                    f.write(self.robots_content)
                
                self._parse_robots_txt()
                return True
            else:
                logger.warning(f"Could not retrieve robots.txt, status: {response.status}")
                return False
                
        except Exception as e:
            logger.error(f"Error fetching robots.txt: {e}")
            return False
    
    def _parse_robots_txt(self):
        """Parse robots.txt content into rules"""
        if not self.robots_content:
            return
        
        current_user_agent = None
        self.rules = {'*': {'disallow': [], 'allow': [], 'crawl_delay': None}}
        
        for line in self.robots_content.split('\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse directives
            if ':' in line:
                directive, value = line.split(':', 1)
                directive = directive.strip().lower()
                value = value.strip()
                
                if directive == 'user-agent':
                    current_user_agent = value
                    if current_user_agent not in self.rules:
                        self.rules[current_user_agent] = {'disallow': [], 'allow': [], 'crawl_delay': None}
                
                elif directive == 'disallow':
                    if current_user_agent:
                        self.rules[current_user_agent]['disallow'].append(value)
                    else:
                        self.rules['*']['disallow'].append(value)
                
                elif directive == 'allow':
                    if current_user_agent:
                        self.rules[current_user_agent]['allow'].append(value)
                    else:
                        self.rules['*']['allow'].append(value)
                
                elif directive == 'crawl-delay':
                    try:
                        delay = float(value)
                        if current_user_agent:
                            self.rules[current_user_agent]['crawl_delay'] = delay
                        else:
                            self.rules['*']['crawl_delay'] = delay
                    except ValueError:
                        logger.warning(f"Invalid crawl-delay value: {value}")
    
    def is_path_allowed(self, path, user_agent='*'):
        """Check if a specific path is allowed for scraping"""
        # Check user-agent specific rules first, then fall back to *
        user_agents_to_check = [user_agent, '*'] if user_agent != '*' else ['*']
        
        for ua in user_agents_to_check:
            if ua in self.rules:
                rules = self.rules[ua]
                
                # Check explicit allow rules first
                for allow_pattern in rules['allow']:
                    if self._path_matches_pattern(path, allow_pattern):
                        return True
                
                # Check disallow rules
                for disallow_pattern in rules['disallow']:
                    if self._path_matches_pattern(path, disallow_pattern):
                        return False
        
        # If no rules match, default to allowed
        return True
    
    def _path_matches_pattern(self, path, pattern):
        """Check if a path matches a robots.txt pattern"""
        if not pattern or pattern == '/':
            return path == '/' if pattern == '/' else True
        
        # Convert robots.txt pattern to regex
        # * matches any sequence of characters
        # $ at the end means exact match
        regex_pattern = re.escape(pattern).replace(r'\*', '.*')
        
        if pattern.endswith('$'):
            regex_pattern = regex_pattern[:-2] + '$'  # Remove escaped $ and add actual $
        
        return bool(re.match(regex_pattern, path))
    
    def get_crawl_delay(self, user_agent='*'):
        """Get recommended crawl delay for user agent"""
        user_agents_to_check = [user_agent, '*'] if user_agent != '*' else ['*']
        
        for ua in user_agents_to_check:
            if ua in self.rules and self.rules[ua]['crawl_delay'] is not None:
                return self.rules[ua]['crawl_delay']
        
        return 1.0  # Default 1 second delay
    
    def check_gradcafe_compliance(self):
        """Specific compliance check for GradCafe scraping"""
        if not self.fetch_robots_txt():
            logger.warning("Could not fetch robots.txt, proceeding with caution")
            return True  # Assume allowed if robots.txt is not accessible
        
        # Paths we plan to scrape
        paths_to_check = [
            '/survey/',
            '/survey/index.php',
            '/search/',
            '/search/index.php'
        ]
        
        compliance_results = {}
        
        for path in paths_to_check:
            is_allowed = self.is_path_allowed(path)
            compliance_results[path] = is_allowed
            
            if is_allowed:
                logger.info(f"✓ Path '{path}' is allowed for scraping")
            else:
                logger.warning(f"✗ Path '{path}' is disallowed for scraping")
        
        # Check crawl delay
        recommended_delay = self.get_crawl_delay()
        logger.info(f"Recommended crawl delay: {recommended_delay} seconds")
        
        # Overall compliance
        all_allowed = all(compliance_results.values())
        
        if all_allowed:
            logger.info("✓ All planned scraping paths are compliant with robots.txt")
        else:
            logger.warning("✗ Some planned scraping paths are not compliant with robots.txt")
        
        # Generate compliance report
        self._generate_compliance_report(compliance_results, recommended_delay)
        
        return all_allowed
    
    def _generate_compliance_report(self, compliance_results, crawl_delay):
        """Generate a detailed compliance report"""
        report = {
            'timestamp': '2024-01-01T00:00:00Z',  # Will be updated in real execution
            'base_url': self.base_url,
            'robots_txt_accessible': self.robots_content is not None,
            'path_compliance': compliance_results,
            'recommended_crawl_delay': crawl_delay,
            'overall_compliant': all(compliance_results.values()) if compliance_results else True,
            'rules_summary': self.rules
        }
        
        try:
            import json
            with open('robots_compliance_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info("Compliance report saved to robots_compliance_report.json")
        except Exception as e:
            logger.error(f"Error saving compliance report: {e}")
    
    def display_robots_content(self):
        """Display the robots.txt content for manual review"""
        if self.robots_content:
            print("=" * 50)
            print("ROBOTS.TXT CONTENT")
            print("=" * 50)
            print(self.robots_content)
            print("=" * 50)
        else:
            print("No robots.txt content available")

def main():
    """Main function for testing robots compliance"""
    print("GradCafe Robots.txt Compliance Checker")
    print("=====================================")
    
    checker = RobotsChecker()
    
    # Display robots.txt content
    if checker.fetch_robots_txt():
        checker.display_robots_content()
    
    # Check compliance
    is_compliant = checker.check_gradcafe_compliance()
    
    if is_compliant:
        print("\n✓ Scraping is compliant with robots.txt")
        print("You may proceed with data collection")
    else:
        print("\n✗ Scraping may not be fully compliant with robots.txt")
        print("Please review the compliance report and adjust scraping strategy")

if __name__ == "__main__":
    main()
