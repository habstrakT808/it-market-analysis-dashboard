# fix_data_cleaning.py
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

def quick_fix_cleaning():
    """Quick fix untuk data cleaning dengan error handling yang lebih baik"""
    
    print("🔧 Quick Fix - Data Cleaning...")
    
    # Load raw data
    print("📥 Loading raw data...")
    raw_jobs = pd.read_csv('data/raw/it_jobs_raw.csv')
    raw_tech = pd.read_csv('data/raw/tech_trends_raw.csv')
    
    # Basic cleaning for jobs
    print("🧹 Basic cleaning...")
    
    # Handle missing values
    jobs_df = raw_jobs.copy()
    
    # Fill missing salaries with median
    jobs_df['salary_min'] = jobs_df['salary_min'].fillna(jobs_df['salary_min'].median())
    jobs_df['salary_max'] = jobs_df['salary_max'].fillna(jobs_df['salary_max'].median())
    
    # Fill missing categorical with mode or default
    jobs_df['industry'] = jobs_df['industry'].fillna('Technology')
    jobs_df['company_size'] = jobs_df['company_size'].fillna('Medium (50-500)')
    jobs_df['employment_type'] = jobs_df['employment_type'].fillna('Full-time')
    jobs_df['remote_option'] = jobs_df['remote_option'].fillna('On-site')
    jobs_df['required_skills'] = jobs_df['required_skills'].fillna('General Programming')
    
    # Remove duplicates
    initial_count = len(jobs_df)
    jobs_df = jobs_df.drop_duplicates()
    jobs_df = jobs_df.drop_duplicates(subset=['company', 'title', 'location'], keep='first')
    final_count = len(jobs_df)
    
    print(f"📉 Removed {initial_count - final_count} duplicates")
    
    # Add derived features
    jobs_df['salary_avg'] = (jobs_df['salary_min'] + jobs_df['salary_max']) / 2
    
    # Salary categories
    jobs_df['salary_category'] = pd.cut(
        jobs_df['salary_min'], 
        bins=[0, 5000000, 10000000, 15000000, float('inf')],
        labels=['Entry (2-5M)', 'Mid (5-10M)', 'Senior (10-15M)', 'Expert (15M+)']
    )
    
    # Basic tech data cleaning
    tech_df = raw_tech.copy()
    tech_df = tech_df.drop_duplicates()
    tech_df = tech_df[tech_df['salary_usd'] > 0]
    tech_df = tech_df[tech_df['salary_usd'] < 500000]
    tech_df['salary_idr'] = tech_df['salary_usd'] * 15000
    
    # Create directories
    os.makedirs('data/processed', exist_ok=True)
    
    # Save cleaned data
    print("💾 Saving cleaned data...")
    jobs_df.to_csv('data/processed/it_jobs_cleaned.csv', index=False)
    tech_df.to_csv('data/processed/tech_trends_cleaned.csv', index=False)
    
    # Create simple quality report
    quality_report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'job_dataset': {
            'total_records': len(jobs_df),
            'total_columns': len(jobs_df.columns),
            'missing_values': int(jobs_df.isnull().sum().sum()),
            'columns': list(jobs_df.columns)
        },
        'tech_dataset': {
            'total_records': len(tech_df),
            'total_columns': len(tech_df.columns),
            'missing_values': int(tech_df.isnull().sum().sum()),
            'unique_technologies': int(tech_df['technology'].nunique())
        },
        'summary': {
            'avg_salary': float(jobs_df['salary_avg'].mean()),
            'salary_range': {
                'min': float(jobs_df['salary_min'].min()),
                'max': float(jobs_df['salary_max'].max())
            },
            'top_locations': jobs_df['location'].value_counts().head().to_dict(),
            'experience_levels': jobs_df['experience_level'].value_counts().to_dict()
        }
    }
    
    # Save quality report with proper serialization
    try:
        # Convert numpy/pandas types to native Python types
        def convert_types(obj):
            if isinstance(obj, dict):
                return {str(k): convert_types(v) for k, v in obj.items()}
            elif isinstance(obj, (np.integer, np.int64)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj
        
        quality_report = convert_types(quality_report)
        
        with open('data/processed/data_quality_report.json', 'w') as f:
            json.dump(quality_report, f, indent=2)
        
        print("✅ Quality report saved!")
        
    except Exception as e:
        print(f"⚠️ Could not save quality report: {e}")
    
    print("\n📊 Cleaning Summary:")
    print(f"✅ Jobs cleaned: {len(jobs_df)} records")
    print(f"✅ Tech trends cleaned: {len(tech_df)} records")
    print(f"✅ Files saved to data/processed/")
    
    # Show sample of cleaned data
    print("\n🔍 Sample cleaned data:")
    print(jobs_df[['title', 'company', 'location', 'salary_avg', 'experience_level']].head())
    
    return jobs_df, tech_df

if __name__ == "__main__":
    jobs_df, tech_df = quick_fix_cleaning()