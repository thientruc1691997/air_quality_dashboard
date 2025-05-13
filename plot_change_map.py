# flake8: noqa
# pylint: skip-file

import plotly.express as px
import pandas as pd
from dash import dcc, html
from data_preprocess import compute_station_averages

def create_station_change_bar_figure(df, stations_df):
    common_pollutants = ['BEN', 'CO', 'EBE', 'NMHC', 'NO_2', 'O_3', 'PM10', 'SO_2', 'TCH', 'TOL']

    avg_2008 = compute_station_averages(df, 2008, common_pollutants)
    avg_2008 = avg_2008.rename(columns={p: f'{p}_2008' for p in common_pollutants})

    avg_2018 = compute_station_averages(df, 2018, common_pollutants)
    avg_2018 = avg_2018.rename(columns={p: f'{p}_2018' for p in common_pollutants})

    merged = pd.merge(avg_2008, avg_2018, on='station', suffixes=('_2008', '_2018'))

    merged['Overall_2008'] = merged[[f'{p}_2008' for p in common_pollutants]].mean(axis=1)
    merged['Overall_2018'] = merged[[f'{p}_2018' for p in common_pollutants]].mean(axis=1)
    merged['Change'] = merged['Overall_2018'] - merged['Overall_2008']

    merged_full = pd.merge(merged, stations_df, left_on='station', right_on='id')

    fig = px.bar(
        merged_full.sort_values('Change', ascending=False),
        x='name', y='Change',
        color='Change', color_continuous_scale='RdYlGn_r',
        hover_data={
            'name': True,
            'Overall_2008': ':.2f',
            'Overall_2018': ':.2f',
            'Change': ':.2f'
        },
        custom_data=['Overall_2008', 'Overall_2018','Change']
    )
    
    fig.update_traces(
        hovertemplate=(
            "<b>Station:</b> %{x}<br>"
            "<b>2008 Average:</b> %{customdata[0]:.2f} μg/m³<br>"
            "<b>2018 Average:</b> %{customdata[1]:.2f} μg/m³<br>"
            "<b>Change (2018-2008):</b> %{customdata[2]:.2f} μg/m³<br>"
            "<extra></extra>"
        )
    )
    
    fig.update_layout(
        xaxis_title='Station', 
        yaxis_title='Pollution Change (2008 - 2018)', 
        xaxis_tickangle=45, 
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)')

    return fig