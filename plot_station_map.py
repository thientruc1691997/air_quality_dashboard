# flake8: noqa
# pylint: skip-file

import plotly.express as px
import pandas as pd
from dash import dcc, html
from data_preprocess import compute_station_averages


def create_station_map_figure_with_custom_hover(df, stations_df):
    common_pollutants = ['BEN', 'CO', 'EBE', 'NMHC', 'NO_2', 'O_3', 'PM10', 'SO_2', 'TCH', 'TOL']
    station_avg = compute_station_averages(df, 2018, common_pollutants)
    merged_df = pd.merge(station_avg, stations_df, left_on='station', right_on='id')
    merged_df['Overall_Avg_Rounded'] = merged_df['Overall_Avg'].round(2)

    for pollutant in common_pollutants:
        if pollutant in merged_df.columns:
            merged_df[pollutant] = merged_df[pollutant].round(2)

    custom_data = []
    hover_texts = []
    for _, row in merged_df.iterrows():
        pollutant_lines = ""
        for pollutant in common_pollutants:
            if pd.notna(row[pollutant]):
                pollutant_lines += f"{pollutant:<8}: {row[pollutant]} μg/m³<br>"

        hover_text = (
            f"<b>{row['name']}</b><br>"
            f"<b>Overall:</b> {row['Overall_Avg_Rounded']} μg/m³<br><br>"
            f"<b>Pollutant Levels:</b><br>{pollutant_lines}"
        )
        hover_texts.append(hover_text)

    fig = px.scatter_mapbox(
        merged_df,
        lat='lat',
        lon='lon',
        size='Overall_Avg',
        color='Overall_Avg',
        color_continuous_scale='YlOrRd',
        size_max=20,
        zoom=10,
        mapbox_style='carto-positron',
        title='Pollution Levels by Station in 2018'
    )

    fig.update_traces(
        hovertemplate='%{customdata}',
        customdata=hover_texts
    )

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Courier New, monospace"
        )
    )

    return fig
