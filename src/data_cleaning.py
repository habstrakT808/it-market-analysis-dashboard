# src/data_cleaning.py
import pandas as pd
import numpy as np
from datetime import datetime
import re

class ITJobDataCleaner:
    def __init__(self):
        self.cleaned_data = None
        self.tech_data = None
        
    def load_raw_data(self):
        """Load raw data dari hasil collection"""
        print("📥 Loading raw data...")
        
        self.raw_jobs = pd.read_csv('data/raw/it_jobs_raw.csv')
        self.raw_tech = pd.read_csv('data/raw/tech_trends_raw.csv')
        
        print(f"✅ Loaded {len(self.raw_jobs)} job records")
        print(f"✅ Loaded {len(self.raw_tech)} tech trend records")
        
        return self.raw_jobs, self.raw_tech
    
    def clean_job_data(self):
        """Comprehensive cleaning untuk job dataset"""
        print("🧹 Cleaning job dataset...")
        
        df = self.raw_jobs.copy()
        
        # 1. Handle missing values
        df = self._handle_missing_values(df)
        
        # 2. Clean salary data
        df = self._clean_salary_data(df)
        
        # 3. Standardize categorical data
        df = self._standardize_categories(df)
        
        # 4. Clean skills data
        df = self._clean_skills_data(df)
        
        # 5. Fix date columns
        df = self._clean_date_columns(df)
        
        # 6. Create derived features
        df = self._create_derived_features(df)
        
        # 7. Remove duplicates
        df = self._remove_duplicates(df)
        
        self.cleaned_jobs = df
        print(f"✅ Job data cleaned: {len(df)} records remaining")
        
        return df
    
    def clean_tech_data(self):
        """Clean technology trends data"""
        print("🧹 Cleaning tech trends dataset...")
        
        df = self.raw_tech.copy()
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Clean technology names
        df['technology'] = df['technology'].str.strip()
        df['technology'] = df['technology'].str.title()
        
        # Filter valid salaries
        df = df[df['salary_usd'] > 0]
        df = df[df['salary_usd'] < 500000]  # Remove outliers
        
        # Convert to IDR (approximate)
        df['salary_idr'] = df['salary_usd'] * 15000  # 1 USD = 15,000 IDR
        
        self.cleaned_tech = df
        print(f"✅ Tech data cleaned: {len(df)} records remaining")
        
        return df
    
    def _handle_missing_values(self, df):
        """Handle missing values dengan strategi yang tepat"""
        print("   🔧 Handling missing values...")
        
        # Fill missing salary dengan median berdasarkan experience level
        for level in df['experience_level'].unique():
            mask = (df['experience_level'] == level)
            
            if df.loc[mask, 'salary_min'].isna().any():
                median_min = df.loc[mask, 'salary_min'].median()
                df.loc[mask, 'salary_min'] = df.loc[mask, 'salary_min'].fillna(median_min)
            
            if df.loc[mask, 'salary_max'].isna().any():
                median_max = df.loc[mask, 'salary_max'].median()
                df.loc[mask, 'salary_max'] = df.loc[mask, 'salary_max'].fillna(median_max)
        
        # Fill missing categorical dengan mode
        categorical_cols = ['industry', 'company_size', 'employment_type', 'remote_option']
        for col in categorical_cols:
            if col in df.columns and df[col].isna().any():
                mode_value = df[col].mode().iloc[0] if not df[col].mode().empty else 'Unknown'
                df[col] = df[col].fillna(mode_value)
        
        # Fill missing skills
        if 'required_skills' in df.columns:
            df['required_skills'] = df['required_skills'].fillna('General Programming')
        
        return df
    
    def _clean_salary_data(self, df):
        """Clean dan validate salary data"""
        print("   💰 Cleaning salary data...")
        
        # Ensure salary_min <= salary_max
        mask = df['salary_min'] > df['salary_max']
        if mask.any():
            # Swap values
            df.loc[mask, ['salary_min', 'salary_max']] = df.loc[mask, ['salary_max', 'salary_min']].values
        
        # Remove unrealistic salaries
        df = df[df['salary_min'] >= 2000000]  # Min 2 juta
        df = df[df['salary_max'] <= 50000000]  # Max 50 juta
        
        # Create salary categories
        df['salary_category'] = pd.cut(
            df['salary_min'], 
            bins=[0, 5000000, 10000000, 15000000, float('inf')],
            labels=['Entry (2-5M)', 'Mid (5-10M)', 'Senior (10-15M)', 'Expert (15M+)']
        )
        
        # Calculate average salary
        df['salary_avg'] = (df['salary_min'] + df['salary_max']) / 2
        
        return df
    
    def _standardize_categories(self, df):
        """Standardize categorical variables"""
        print("   📊 Standardizing categories...")
        
        # Standardize experience levels
        exp_mapping = {
            'junior': 'Junior',
            'mid': 'Mid',
            'senior': 'Senior',
            'lead': 'Senior'
        }
        
        # Standardize company sizes
        size_mapping = {
            'startup': 'Startup (<50)',
            'small': 'Startup (<50)',
            'medium': 'Medium (50-500)',
            'large': 'Large (500+)',
            'enterprise': 'Large (500+)'
        }
        
        # Apply mappings
        df['experience_level'] = df['experience_level'].str.lower().map(exp_mapping).fillna(df['experience_level'])
        
        # Clean location names
        df['location'] = df['location'].str.title()
        df['location'] = df['location'].str.replace('Dki Jakarta', 'Jakarta')
        df['location'] = df['location'].str.replace('Yogyakarta', 'Yogya')
        
        return df
    
    def _clean_skills_data(self, df):
        """Clean dan standardize skills data"""
        print("   🛠️ Cleaning skills data...")
        
        # Standardize skill names
        skill_mapping = {
            'javascript': 'JavaScript',
            'python': 'Python',
            'java': 'Java',
            'php': 'PHP',
            'react': 'React',
            'vue': 'Vue.js',
            'angular': 'Angular',
            'node': 'Node.js',
            'nodejs': 'Node.js',
            'mysql': 'MySQL',
            'postgresql': 'PostgreSQL',
            'mongodb': 'MongoDB'
        }
        
        def clean_skills(skills_str):
            if pd.isna(skills_str) or skills_str == '':
                return 'General Programming'
            
            # Split skills
            skills = [skill.strip() for skill in str(skills_str).split(',')]
            
            # Clean each skill
            cleaned_skills = []
            for skill in skills:
                skill_lower = skill.lower()
                cleaned_skill = skill_mapping.get(skill_lower, skill)
                if cleaned_skill not in cleaned_skills:
                    cleaned_skills.append(cleaned_skill)
            
            return ', '.join(cleaned_skills)
        
        df['required_skills'] = df['required_skills'].apply(clean_skills)
        
        # Create skill categories
        def categorize_skills(skills_str):
            skills_lower = str(skills_str).lower()
            
            categories = []
            if any(skill in skills_lower for skill in ['react', 'vue', 'angular', 'javascript', 'html', 'css']):
                categories.append('Frontend')
            if any(skill in skills_lower for skill in ['python', 'java', 'php', 'node', 'django', 'laravel']):
                categories.append('Backend')
            if any(skill in skills_lower for skill in ['mysql', 'postgresql', 'mongodb', 'sql']):
                categories.append('Database')
            if any(skill in skills_lower for skill in ['docker', 'kubernetes', 'aws', 'azure', 'devops']):
                categories.append('DevOps')
            if any(skill in skills_lower for skill in ['pandas', 'numpy', 'tableau', 'powerbi', 'analytics']):
                categories.append('Data')
            
            return ', '.join(categories) if categories else 'General'
        
        df['skill_category'] = df['required_skills'].apply(categorize_skills)
        
        return df
    
    def _clean_date_columns(self, df):
        """Clean date columns"""
        print("   📅 Cleaning date columns...")
        
        date_columns = ['posted_date', 'application_deadline', 'data_collection_date']
        
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Calculate days since posted
        if 'posted_date' in df.columns:
            df['days_since_posted'] = (datetime.now() - df['posted_date']).dt.days
        
        return df
    
    def _create_derived_features(self, df):
        """Create additional useful features"""
        print("   ⚙️ Creating derived features...")
        
        # Salary competitiveness score (compared to market average by level)
        level_avg_salary = df.groupby('experience_level')['salary_avg'].mean()
        df['salary_competitiveness'] = df.apply(
            lambda row: row['salary_avg'] / level_avg_salary[row['experience_level']], 
            axis=1
        )
        
        # Location tier (based on typical salary levels)
        tier_1_cities = ['Jakarta', 'Remote']
        tier_2_cities = ['Bandung', 'Surabaya', 'Yogya']
        
        def get_city_tier(location):
            if location in tier_1_cities:
                return 'Tier 1'
            elif location in tier_2_cities:
                return 'Tier 2'
            else:
                return 'Tier 3'
        
        df['city_tier'] = df['location'].apply(get_city_tier)
        
        # Job attractiveness score (combination of factors)
        def calculate_attractiveness(row):
            score = 0
            
            # Salary factor (30%)
            score += (row['salary_competitiveness'] - 1) * 30
            
            # Remote option factor (20%)
            if row['remote_option'] in ['Remote', 'Hybrid']:
                score += 20
            
            # Company size factor (10%)
            if row['company_size'] == 'Large (500+)':
                score += 10
            elif row['company_size'] == 'Medium (50-500)':
                score += 5
            
            # Experience match factor (40%)
            if row['experience_level'] == 'Mid':
                score += 40  # Most balanced
            elif row['experience_level'] == 'Senior':
                score += 35
            else:
                score += 30
            
            return max(0, min(100, score))  # Normalize to 0-100
        
        df['attractiveness_score'] = df.apply(calculate_attractiveness, axis=1)
        
        return df
    
    def _remove_duplicates(self, df):
        """Remove duplicate records"""
        print("   🔄 Removing duplicates...")
        
        initial_count = len(df)
        
        # Remove exact duplicates
        df = df.drop_duplicates()
        
        # Remove near-duplicates (same company, title, location)
        df = df.drop_duplicates(subset=['company', 'title', 'location'], keep='first')
        
        final_count = len(df)
        removed = initial_count - final_count
        
        if removed > 0:
            print(f"   📉 Removed {removed} duplicate records")
        
        return df
    
    def generate_data_quality_report(self):
        """Generate comprehensive data quality report"""
        print("📋 Generating data quality report...")
        
        report = {
            'timestamp': datetime.now(),
            'job_dataset': {
                'total_records': len(self.cleaned_jobs),
                'total_columns': len(self.cleaned_jobs.columns),
                'missing_values': self.cleaned_jobs.isnull().sum().sum(),
                'duplicate_records': 0,
                'data_types': self.cleaned_jobs.dtypes.value_counts().to_dict()
            },
            'tech_dataset': {
                'total_records': len(self.cleaned_tech),
                'total_columns': len(self.cleaned_tech.columns),
                'missing_values': self.cleaned_tech.isnull().sum().sum(),
                'unique_technologies': self.cleaned_tech['technology'].nunique()
            },
            'business_insights': {
                'salary_range': {
                    'min': self.cleaned_jobs['salary_min'].min(),
                    'max': self.cleaned_jobs['salary_max'].max(),
                    'average': self.cleaned_jobs['salary_avg'].mean()
                },
                'top_locations': self.cleaned_jobs['location'].value_counts().head().to_dict(),
                'top_skills': self._get_top_skills(),
                'experience_distribution': self.cleaned_jobs['experience_level'].value_counts().to_dict()
            }
        }
        
        return report
    
    def _get_top_skills(self):
        """Extract top skills from dataset"""
        all_skills = []
        for skills_str in self.cleaned_jobs['required_skills'].dropna():
            skills = [skill.strip() for skill in str(skills_str).split(',')]
            all_skills.extend(skills)
        
        skill_counts = pd.Series(all_skills).value_counts()
        return skill_counts.head(10).to_dict()
    
    def save_cleaned_data(self):
        """Save cleaned datasets"""
        print("💾 Saving cleaned data...")
        
        # Save main dataset
        self.cleaned_jobs.to_csv('data/processed/it_jobs_cleaned.csv', index=False)
        self.cleaned_tech.to_csv('data/processed/tech_trends_cleaned.csv', index=False)
        
        # Save data quality report
        report = self.generate_data_quality_report()
        
        import json
        with open('data/processed/data_quality_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print("✅ Cleaned data saved successfully!")
        print(f"📁 Job dataset: data/processed/it_jobs_cleaned.csv ({len(self.cleaned_jobs)} records)")
        print(f"📁 Tech dataset: data/processed/tech_trends_cleaned.csv ({len(self.cleaned_tech)} records)")
        print(f"📁 Quality report: data/processed/data_quality_report.json")
        
        return self.cleaned_jobs, self.cleaned_tech

def main():
    """Main function untuk data cleaning"""
    print("🧹 Starting Data Cleaning Process...")
    print("=" * 50)
    
    # Initialize cleaner
    cleaner = ITJobDataCleaner()
    
    # Load raw data
    raw_jobs, raw_tech = cleaner.load_raw_data()
    
    # Clean datasets
    cleaned_jobs = cleaner.clean_job_data()
    cleaned_tech = cleaner.clean_tech_data()
    
    # Generate and save results
    final_jobs, final_tech = cleaner.save_cleaned_data()
    
    # Print summary
    print("\n📊 Cleaning Summary:")
    print(f"Jobs: {len(raw_jobs)} → {len(final_jobs)} records")
    print(f"Tech: {len(raw_tech)} → {len(final_tech)} records")
    
    print("\n✅ Data cleaning completed successfully!")
    
    return final_jobs, final_tech

if __name__ == "__main__":
    main()