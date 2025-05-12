# flake8: noqa
# pylint: skip-file
import pandas as pd

#H1
def compute_annual_averages(df, pollutants):
    annual_avg = df.groupby('year')[pollutants].mean().reset_index()
    melted = annual_avg.melt(id_vars='year', value_vars=pollutants,
                             var_name='Pollutant', value_name='Average Concentration')
    return melted

#H2
def compute_station_averages(df, year, pollutants):
    filtered = df[df['year'] == year].copy()

    # # Convert mg/m³ to μg/m³
    # mg_cols = ['CO', 'CH4', 'NMHC', 'TCH']
    # for col in mg_cols:
    #     if col in filtered.columns:
    #         filtered[col] = pd.to_numeric(filtered[col], errors='coerce') * 1000

    # Compute mean per station
    result = filtered.groupby('station')[pollutants].mean().reset_index()

    # Compute overall average across all selected pollutants
    result['Overall_Avg'] = result[pollutants].mean(axis=1)

    return result

