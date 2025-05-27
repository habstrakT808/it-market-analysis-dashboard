# verify_data.py
import pandas as pd
import os

def verify_collected_data():
    """Verify collected data quality"""
    
    print("🔍 Verifying collected data...")
    
    # Check if files exist
    files_to_check = [
        'data/raw/it_jobs_raw.csv',
        'data/raw/tech_trends_raw.csv'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
            
            # Load and check data
            df = pd.read_csv(file_path)
            print(f"   📊 Shape: {df.shape}")
            print(f"   📋 Columns: {list(df.columns)}")
            print(f"   🔢 Data types: {df.dtypes.value_counts().to_dict()}")
            print()
        else:
            print(f"❌ {file_path} not found")
    
    # Detailed analysis of main dataset
    if os.path.exists('data/raw/it_jobs_raw.csv'):
        df = pd.read_csv('data/raw/it_jobs_raw.csv')
        
        print("📈 Main Dataset Analysis:")
        print(f"   Total jobs: {len(df)}")
        print(f"   Unique companies: {df['company'].nunique()}")
        print(f"   Unique locations: {df['location'].nunique()}")
        print(f"   Salary range: {df['salary_min'].min():,.0f} - {df['salary_max'].max():,.0f}")
        print(f"   Missing values: {df.isnull().sum().sum()}")
        
        print("\n🏢 Top 5 Companies:")
        print(df['company'].value_counts().head())
        
        print("\n📍 Top 5 Locations:")
        print(df['location'].value_counts().head())
        
        print("\n💼 Job Titles Distribution:")
        print(df['title'].value_counts().head())

if __name__ == "__main__":
    verify_collected_data()