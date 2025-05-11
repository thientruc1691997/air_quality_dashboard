# flake8: noqa

import pandas as pd
import os

def load_pollution_data(filepath):
    df = pd.read_parquet(filepath)  # Changed from read_csv to read_parquet
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
    
    return df

def load_station_metadata(filepath):
    return pd.read_parquet(filepath)  # Changed from read_csv to read_parquet


