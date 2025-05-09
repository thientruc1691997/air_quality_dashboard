# flake8: noqa

import pandas as pd
import os

base_path = "/Users/nguyentruc/Desktop/UHasselt/Data Visualization/Project/VDS2425_Madrid/"
years = list(range(2001, 2019))

summary_data = []
pollutants_per_year = {}

for year in years:
    file_path = os.path.join(base_path, f"madrid_{year}.csv")
    try:
        df = pd.read_csv(file_path)
        
        num_rows = df.shape[0]
        num_cols = df.shape[1]
        
        pollutant_cols = [col for col in df.columns if col.lower() not in ['date', 'station']]
        
        summary_data.append({
            'Year': year,
            'NumRows': num_rows,
            'NumVars': num_cols,
            'Pollutants': pollutant_cols
        })
        
        pollutants_per_year[year] = set(pollutant_cols)
        
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Convert summary to DataFrame
summary_df = pd.DataFrame(summary_data)
summary_df.set_index('Year', inplace=True)

# Print summary
print("\n=== SUMMARY TABLE ===")
print(summary_df[['NumRows', 'NumVars']])
print("\nPollutants per year:")
for year, pollutants in pollutants_per_year.items():
    print(f"{year}: {', '.join(pollutants)}")

# Compare pollutant sets
years_same_pollutants = []
base_pollutants = None
for year, pollutants in pollutants_per_year.items():
    if base_pollutants is None:
        base_pollutants = pollutants
        years_same_pollutants.append(year)
    elif pollutants == base_pollutants:
        years_same_pollutants.append(year)

print("\nYears with identical pollutant columns:")
print(years_same_pollutants)

# Identify years with different columns
for year, pollutants in pollutants_per_year.items():
    if pollutants != base_pollutants:
        diff = pollutants.symmetric_difference(base_pollutants)
        print(f"⚠️ Year {year} differs by: {diff}")

# Compute intersection of all sets
common_pollutants = set.intersection(*pollutants_per_year.values())

# Print results
print("\n✅ Common pollutants across ALL years:")
print(", ".join(sorted(common_pollutants)))



