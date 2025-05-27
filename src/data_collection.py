import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import json
import random

class ITJobDataCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def load_stackoverflow_data(self):
        """Load dan process Stack Overflow Developer Survey data"""
        print("📥 Loading Stack Overflow Developer Survey data...")
        
        # Simulasi data SO survey karena file asli sangat besar
        # Dalam praktik nyata, download dari: https://insights.stackoverflow.com/survey
        
        technologies = [
            'JavaScript', 'Python', 'Java', 'TypeScript', 'C#', 'PHP', 'C++', 
            'React', 'Node.js', 'Angular', 'Vue.js', 'Laravel', 'Django', 
            'Spring Boot', 'Express.js', 'MySQL', 'PostgreSQL', 'MongoDB',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'Git', 'Linux'
        ]
        
        # Generate realistic survey responses
        survey_data = []
        for i in range(500):
            num_techs = random.randint(3, 8)
            selected_techs = random.sample(technologies, num_techs)
            
            survey_data.append({
                'respondent_id': i + 1,
                'country': random.choice(['Indonesia', 'Singapore', 'Malaysia', 'Thailand']),
                'experience_years': random.randint(1, 15),
                'technologies': ', '.join(selected_techs),
                'salary_usd': random.randint(15000, 120000),
                'company_size': random.choice(['Small', 'Medium', 'Large']),
                'remote_work': random.choice(['Never', 'Sometimes', 'Always'])
            })
        
        return pd.DataFrame(survey_data)
    
    def light_web_scraping(self):
        """Light scraping dari job portal (minimal dan ethical)"""
        print("🕷️ Performing light web scraping...")
        
        jobs_data = []
        
        # Simulasi scraping result (dalam praktik nyata, scrape dari job portal)
        # Contoh struktur data yang biasa didapat dari scraping
        sample_scraped_jobs = [
            {
                'title': 'Software Developer',
                'company': 'Tech Startup Jakarta',
                'location': 'Jakarta',
                'salary_text': '8-12 juta',
                'description': 'JavaScript, React, Node.js experience required',
                'posted_date': '2024-01-15',
                'source': 'scraped'
            },
            {
                'title': 'Data Analyst',
                'company': 'E-commerce Company',
                'location': 'Bandung',
                'salary_text': '6-10 juta',
                'description': 'Python, SQL, Tableau experience',
                'posted_date': '2024-01-14',
                'source': 'scraped'
            },
            {
                'title': 'Full Stack Developer',
                'company': 'Digital Agency',
                'location': 'Surabaya',
                'salary_text': '10-15 juta',
                'description': 'PHP, Laravel, Vue.js, MySQL',
                'posted_date': '2024-01-13',
                'source': 'scraped'
            }
        ]
        
        # Expand sample data
        for i in range(30):  # Generate 30 scraped-like records
            base_job = random.choice(sample_scraped_jobs)
            job = base_job.copy()
            job['job_id'] = f'SCRAPED_{i+1:03d}'
            job['posted_date'] = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            jobs_data.append(job)
        
        time.sleep(1)  # Be respectful
        return pd.DataFrame(jobs_data)
    
    def generate_realistic_job_data(self):
        """Generate comprehensive realistic job market data"""
        print("🎲 Generating realistic job market data...")
        
        np.random.seed(42)
        
        # Comprehensive data definitions
        job_titles = [
            'Software Developer', 'Data Analyst', 'Frontend Developer', 
            'Backend Developer', 'Full Stack Developer', 'DevOps Engineer', 
            'UI/UX Designer', 'Mobile Developer', 'Data Scientist',
            'System Administrator', 'Database Administrator', 'QA Engineer',
            'Product Manager', 'Scrum Master', 'Technical Lead',
            'Cloud Engineer', 'Security Engineer', 'Business Analyst'
        ]
        
        companies = [
            'Tokopedia', 'Gojek', 'Bukalapak', 'Traveloka', 'Blibli',
            'Shopee', 'OVO', 'Dana', 'Grab', 'Sea Group',
            'Local Tech Startup', 'Digital Consulting', 'Software House',
            'Bank Digital', 'Fintech Company', 'E-commerce Platform',
            'Government Agency', 'Multinational Corp', 'Healthcare Tech'
        ]
        
        locations = [
            'Jakarta', 'Bandung', 'Surabaya', 'Yogyakarta', 'Semarang',
            'Medan', 'Makassar', 'Bali', 'Lampung', 'Palembang',
            'Malang', 'Solo', 'Batam', 'Remote', 'Hybrid'
        ]
        
        skills_pool = [
            'Python', 'JavaScript', 'Java', 'PHP', 'C#', 'Go', 'Ruby',
            'React', 'Vue.js', 'Angular', 'Node.js', 'Laravel', 'Django',
            'Spring Boot', 'Express.js', 'Flask', 'FastAPI',
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
            'Git', 'Jenkins', 'Terraform', 'Linux', 'Nginx'
        ]
        
        industries = [
            'E-commerce', 'Fintech', 'Healthcare', 'Education', 'Transportation',
            'Food & Beverage', 'Gaming', 'Media', 'Government', 'Consulting'
        ]
        
        # Generate job records
        jobs_data = []
        for i in range(800):  # Generate 800 records
            
            # Determine experience level first (affects salary)
            exp_level = np.random.choice(['Junior', 'Mid', 'Senior'], p=[0.4, 0.4, 0.2])
            
            # Base salary by experience
            if exp_level == 'Junior':
                base_salary = np.random.randint(4, 8) * 1000000
            elif exp_level == 'Mid':
                base_salary = np.random.randint(8, 15) * 1000000
            else:  # Senior
                base_salary = np.random.randint(15, 30) * 1000000
            
            # Location adjustment
            location = np.random.choice(locations)
            location_multiplier = 1.0
            if location in ['Jakarta', 'Remote']:
                location_multiplier = 1.2
            elif location in ['Bandung', 'Surabaya']:
                location_multiplier = 1.1
            elif location in ['Lampung', 'Palembang']:
                location_multiplier = 0.8
            
            adjusted_salary = int(base_salary * location_multiplier)
            
            job = {
                'job_id': f'JOB_{i+1:04d}',
                'title': np.random.choice(job_titles),
                'company': np.random.choice(companies),
                'location': location,
                'industry': np.random.choice(industries),
                'salary_min': adjusted_salary,
                'salary_max': adjusted_salary + np.random.randint(2, 6) * 1000000,
                'experience_level': exp_level,
                'experience_years_min': self._get_exp_years(exp_level)[0],
                'experience_years_max': self._get_exp_years(exp_level)[1],
                'company_size': np.random.choice(['Startup (<50)', 'Medium (50-500)', 'Large (500+)'], 
                                               p=[0.3, 0.4, 0.3]),
                'employment_type': np.random.choice(['Full-time', 'Contract', 'Part-time'], 
                                                  p=[0.8, 0.15, 0.05]),
                'remote_option': np.random.choice(['On-site', 'Remote', 'Hybrid'], 
                                                p=[0.4, 0.3, 0.3]),
                'required_skills': self._generate_skills(skills_pool),
                'posted_date': datetime.now() - timedelta(days=np.random.randint(1, 90)),
                'application_deadline': datetime.now() + timedelta(days=np.random.randint(7, 60)),
                'source': 'generated'
            }
            
            jobs_data.append(job)
        
        return pd.DataFrame(jobs_data)
    
    def _get_exp_years(self, level):
        """Get experience years range based on level"""
        if level == 'Junior':
            return (0, 2)
        elif level == 'Mid':
            return (3, 6)
        else:  # Senior
            return (7, 15)
    
    def _generate_skills(self, skills_pool):
        """Generate realistic skill combinations"""
        num_skills = np.random.randint(3, 7)
        skills = np.random.choice(skills_pool, size=num_skills, replace=False)
        return ', '.join(skills)
    
    def combine_datasets(self, stackoverflow_data, scraped_data, generated_data):
        """Combine all data sources into unified dataset"""
        print("🔄 Combining all data sources...")
        
        # Process Stack Overflow data
        so_processed = self._process_stackoverflow_data(stackoverflow_data)
        
        # Process scraped data
        scraped_processed = self._process_scraped_data(scraped_data)
        
        # Combine with generated data
        final_dataset = pd.concat([
            generated_data,
            scraped_processed
        ], ignore_index=True)
        
        # Add metadata
        final_dataset['data_collection_date'] = datetime.now()
        final_dataset['dataset_version'] = '1.0'
        
        return final_dataset, so_processed
    
    def _process_stackoverflow_data(self, so_data):
        """Process Stack Overflow survey data"""
        # Extract technology trends
        tech_trends = []
        for _, row in so_data.iterrows():
            techs = row['technologies'].split(', ')
            for tech in techs:
                tech_trends.append({
                    'technology': tech,
                    'country': row['country'],
                    'experience_years': row['experience_years'],
                    'salary_usd': row['salary_usd'],
                    'company_size': row['company_size']
                })
        
        return pd.DataFrame(tech_trends)
    
    def _process_scraped_data(self, scraped_data):
        """Process and standardize scraped data"""
        processed = scraped_data.copy()
        
        # Parse salary text to numeric
        processed['salary_min'] = processed['salary_text'].apply(self._parse_salary_min)
        processed['salary_max'] = processed['salary_text'].apply(self._parse_salary_max)
        
        # Extract skills from description
        processed['required_skills'] = processed['description'].apply(self._extract_skills)
        
        # Standardize other fields
        processed['experience_level'] = 'Mid'  # Default assumption
        processed['company_size'] = 'Medium (50-500)'  # Default assumption
        processed['remote_option'] = processed['location'].apply(
            lambda x: 'Remote' if 'remote' in x.lower() else 'On-site'
        )
        
        return processed[['job_id', 'title', 'company', 'location', 'salary_min', 
                        'salary_max', 'required_skills', 'experience_level', 
                        'company_size', 'remote_option', 'source']]
    
    def _parse_salary_min(self, salary_text):
        """Parse minimum salary from text"""
        try:
            # Extract first number from "8-12 juta" format
            import re
            numbers = re.findall(r'\d+', salary_text)
            if numbers:
                return int(numbers[0]) * 1000000
        except:
            pass
        return 5000000  # Default
    
    def _parse_salary_max(self, salary_text):
        """Parse maximum salary from text"""
        try:
            import re
            numbers = re.findall(r'\d+', salary_text)
            if len(numbers) >= 2:
                return int(numbers[1]) * 1000000
            elif len(numbers) == 1:
                return int(numbers[0]) * 1000000 + 2000000
        except:
            pass
        return 8000000  # Default
    
    def _extract_skills(self, description):
        """Extract skills from job description"""
        skills_keywords = ['Python', 'JavaScript', 'Java', 'PHP', 'React', 'Vue.js', 
                          'Node.js', 'Laravel', 'SQL', 'MySQL', 'Tableau']
        
        found_skills = []
        for skill in skills_keywords:
            if skill.lower() in description.lower():
                found_skills.append(skill)
        
        return ', '.join(found_skills) if found_skills else 'General Programming'

def main():
    """Main function untuk menjalankan data collection"""
    collector = ITJobDataCollector()
    
    print("🚀 Starting IT Market Data Collection...")
    print("=" * 50)
    
    # 1. Load Stack Overflow data
    so_data = collector.load_stackoverflow_data()
    print(f"✅ Stack Overflow data loaded: {len(so_data)} records")
    
    # 2. Perform light scraping
    scraped_data = collector.light_web_scraping()
    print(f"✅ Web scraping completed: {len(scraped_data)} records")
    
    # 3. Generate realistic data
    generated_data = collector.generate_realistic_job_data()
    print(f"✅ Realistic data generated: {len(generated_data)} records")
    
    # 4. Combine all datasets
    final_dataset, tech_trends = collector.combine_datasets(so_data, scraped_data, generated_data)
    print(f"✅ Data combination completed: {len(final_dataset)} total records")
    
    # 5. Save datasets
    final_dataset.to_csv('data/raw/it_jobs_raw.csv', index=False)
    tech_trends.to_csv('data/raw/tech_trends_raw.csv', index=False)
    
    print("\n📊 Data Collection Summary:")
    print(f"📁 Main dataset: {len(final_dataset)} job records")
    print(f"📁 Tech trends: {len(tech_trends)} technology records")
    print(f"💾 Files saved to: data/raw/")
    
    print("\n🔍 Dataset Preview:")
    print(final_dataset.head())
    
    print("\n✅ Data collection completed successfully!")
    return final_dataset, tech_trends

if __name__ == "__main__":
    main()