# flake8: noqa
# pylint: skip-file

import plotly.express as px
import pandas as pd

def create_pollution_trend_figure_with_filters(df, selected_years, selected_pollutants):
    # Filter by selected years
    df_filtered = df[(df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]

    # Group by year and compute average only for selected pollutants
    annual_avg = df_filtered.groupby('year')[selected_pollutants].mean().reset_index()

    # Melt for long format
    melted = annual_avg.melt(id_vars='year', var_name='Pollutant', value_name='Average Concentration')

    # Create line plot
    fig = px.line(
        melted, x='year', y='Average Concentration', color='Pollutant',
        markers=True, title=f'Average Annual Pollution in Madrid ({selected_years[0]}–{selected_years[1]})'
    )

    return fig
