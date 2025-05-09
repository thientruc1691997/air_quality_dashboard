# flake8: noqa
# pylint: skip-file

#H1
def compute_annual_averages(df, pollutants):
    annual_avg = df.groupby('year')[pollutants].mean().reset_index()
    melted = annual_avg.melt(id_vars='year', value_vars=pollutants,
                             var_name='Pollutant', value_name='Average Concentration')
    return melted

#H2
def compute_station_averages(df, year, pollutants):
    df_year = df[df['year'] == year]
    station_avg = df_year.groupby('station')[pollutants].mean().reset_index()
    station_avg['Overall_Avg'] = station_avg[pollutants].mean(axis=1)
    return station_avg
