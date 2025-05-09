# flake8: noqa

import pandas as pd
import os

base_path = "/Users/nguyentruc/Desktop/UHasselt/Data Visualization/Project/VDS2425_Madrid/"
years = list(range(2001, 2019))

# Load station metadata
stations_df = pd.read_csv(os.path.join(base_path, 'stations.csv'))
station_ids = stations_df['id'].unique()

summary = []

for year in years:
    file_path = os.path.join(base_path, f"madrid_{year}.csv")
    try:
        df = pd.read_csv(file_path)
        unique_stations = df['station'].unique()
        total_stations = len(unique_stations)
        
        # Check which stations exist in metadata
        matched_stations = [s for s in unique_stations if s in station_ids]
        num_matched = len(matched_stations)
        
        percent_mapped = (num_matched / total_stations) * 100 if total_stations > 0 else 0
        
        summary.append({
            'Year': year,
            'TotalStations': total_stations,
            'MappedStations': num_matched,
            'PercentMapped': round(percent_mapped, 2)
        })
        
    except Exception as e:
        print(f"Error processing year {year}: {e}")

# Create summary DataFrame
summary_df = pd.DataFrame(summary)
print(summary_df)

# Optionally save to CSV
summary_df.to_csv(os.path.join(base_path, 'station_mapping_summary.csv'), index=False)
