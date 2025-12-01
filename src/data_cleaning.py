import pandas as pd
import numpy as np
import os

def clean_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    try:
        df = pd.read_csv(input_path, sep='\t') # GBIF data is often tab-separated, but let's check. 
        # The user file is .csv, usually comma. But let's try comma first, if fail then tab.
        # Based on previous output: "gbifID,datasetKey..." it looks like comma separated.
    except:
        pass
    
    df = pd.read_csv(input_path)
    
    print(f"Initial shape: {df.shape}")
    
    # 1. Handle missing values
    print("Handling missing values...")
    # stateProvince
    df['stateProvince'] = df['stateProvince'].fillna('Unknown')
    
    # depth: Ensure numeric, coerce errors to NaN
    df['depth'] = pd.to_numeric(df['depth'], errors='coerce')
    
    # 2. Parse and format dates
    print("Parsing dates...")
    # Convert eventDate to datetime
    df['eventDate'] = pd.to_datetime(df['eventDate'], errors='coerce')
    
    # Fill year/month if missing from eventDate
    mask_year_missing = df['year'].isna()
    df.loc[mask_year_missing, 'year'] = df.loc[mask_year_missing, 'eventDate'].dt.year
    
    mask_month_missing = df['month'].isna()
    df.loc[mask_month_missing, 'month'] = df.loc[mask_month_missing, 'eventDate'].dt.month
    
    # Drop rows where year is still missing (optional, but good for temporal analysis)
    initial_count = len(df)
    df = df.dropna(subset=['year'])
    print(f"Dropped {initial_count - len(df)} rows with missing year.")
    
    # 3. Filter for specific kingdoms (Check distribution first)
    print("Kingdom distribution:")
    print(df['kingdom'].value_counts())
    
    # 4. Normalize and validate coordinates
    print("Validating coordinates...")
    # Ensure numeric
    df['decimalLatitude'] = pd.to_numeric(df['decimalLatitude'], errors='coerce')
    df['decimalLongitude'] = pd.to_numeric(df['decimalLongitude'], errors='coerce')
    
    # Drop rows with missing coordinates
    df = df.dropna(subset=['decimalLatitude', 'decimalLongitude'])
    
    # Filter valid range
    df = df[
        (df['decimalLatitude'] >= -90) & (df['decimalLatitude'] <= 90) &
        (df['decimalLongitude'] >= -180) & (df['decimalLongitude'] <= 180)
    ]
    
    print(f"Shape after cleaning: {df.shape}")
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    input_file = r"c:\Users\ASUS\Desktop\Biodiversity\dataset_5.csv"
    output_file = r"c:\Users\ASUS\Desktop\Biodiversity\data\cleaned_dataset.csv"
    clean_data(input_file, output_file)
