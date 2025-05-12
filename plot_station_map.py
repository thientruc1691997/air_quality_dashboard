# flake8: noqa
# pylint: skip-file

import plotly.express as px
import pandas as pd
from dash import dcc, html
from data_preprocess import compute_station_averages


def create_station_map_figure_with_custom_hover(df, stations_df):
    common_pollutants = ['BEN', 'CO', 'EBE', 'NMHC', 'NO_2', 'O_3', 'PM10', 'SO_2', 'TCH', 'TOL']
    mg_cols = ['CO', 'CH4', 'NMHC', 'TCH']

    # Compute average per station for 2018
    station_avg = compute_station_averages(df, 2018, common_pollutants)
    merged_df = pd.merge(station_avg, stations_df, left_on='station', right_on='id')

    # Convert mg → μg for specific columns (if they exist in station_avg)
    for col in mg_cols:
        if col in merged_df.columns:
            merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce') * 1000

    # Round values for display
    for pollutant in common_pollutants:
        if pollutant in merged_df.columns:
            merged_df[pollutant] = merged_df[pollutant].round(2)

    merged_df['Overall_Avg_Rounded'] = merged_df['Overall_Avg'].round(2)

    # Build custom hover HTML
    custom_data = []
    for _, row in merged_df.iterrows():
        pollutant_lines = ""
        for pollutant in common_pollutants:
            if pd.notna(row[pollutant]):
                pollutant_lines += f"<b>{pollutant}</b>: {row[pollutant]} μg/m³<br>"

        hover_text = (
            f"<b>Station:</b> {row['name']}<br>"
            f"<b>Overall:</b> {row['Overall_Avg_Rounded']} μg/m³<br><br>"
            f"<b>Pollutant Levels:</b><br>{pollutant_lines}"
        )
        custom_data.append(hover_text)

    # Plot
    fig = px.scatter_mapbox(
        merged_df,
        lat='lat',
        lon='lon',
        size='Overall_Avg',
        color='Overall_Avg',
        color_continuous_scale='YlOrRd',
        size_max=20,
        zoom=10,
        mapbox_style='carto-positron'
    )

    fig.update_traces(
        hovertemplate="%{customdata}<extra></extra>",
        customdata=custom_data
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial"
        )
    )

    return fig
