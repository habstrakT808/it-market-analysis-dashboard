# run_data_collection.py
import sys
import os

# Add src to path
sys.path.append('src')

from data_collection import main

if __name__ == "__main__":
    # Run data collection
    job_data, tech_data = main()
    
    print(f"\n📈 Data Collection Results:")
    print(f"Jobs dataset shape: {job_data.shape}")
    print(f"Tech trends shape: {tech_data.shape}")
    
    print(f"\n📋 Sample job record:")
    print(job_data.iloc[0].to_dict())