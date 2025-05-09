# flake8: noqa

import pandas as pd
import os

base_path = "/Users/nguyentruc/Desktop/UHasselt/Data Visualization/Project/VDS2425_Madrid/"
years = list(range(2001, 2019))

# Collect all results
missing_value_station = []
missing_value_date = []
missing_value_station_hour = []

for year in years:
    file_path = os.path.join(base_path, f"madrid_{year}.csv")
    df = pd.read_csv(file_path)
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['hour'] = df['date'].dt.hour
    df['date_only'] = df['date'].dt.date
    
    pollutant_cols = [col for col in df.columns if col.lower() not in ['date', 'station', 'hour', 'date_only']]
    
    # Missing per station
    m_station = df.groupby('station')[pollutant_cols].apply(lambda x: x.isna().mean() * 100).reset_index()
    m_station['Year'] = year
    missing_value_station.append(m_station)
    
    # Missing per date
    m_date = df.groupby('date_only')[pollutant_cols].apply(lambda x: x.isna().mean() * 100).reset_index()
    m_date['Year'] = year
    missing_value_date.append(m_date)
    
    # Missing per station + hour
    m_station_hour = df.groupby(['station', 'hour'])[pollutant_cols].apply(lambda x: x.isna().mean() * 100).reset_index()
    m_station_hour['Year'] = year
    missing_value_station_hour.append(m_station_hour)

# Combine all years
missing_station_df = pd.concat(missing_value_station, ignore_index=True)
missing_date_df = pd.concat(missing_value_date, ignore_index=True)
missing_station_hour_df = pd.concat(missing_value_station_hour, ignore_index=True)

# Save results to CSV if needed
missing_station_df.to_csv(os.path.join(base_path, 'missing_by_station.csv'), index=False)
missing_date_df.to_csv(os.path.join(base_path, 'missing_by_date.csv'), index=False)
missing_station_hour_df.to_csv(os.path.join(base_path, 'missing_by_station_hour.csv'), index=False)

print("✅ Missingness summaries saved!")
