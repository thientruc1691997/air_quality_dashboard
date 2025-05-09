# flake8: noqa

import pandas as pd


def load_pollution_data(filepath):
    df = pd.read_csv(filepath)
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
    
    return df

def load_station_metadata(filepath):
    return pd.read_csv(filepath)
