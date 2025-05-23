# flake8: noqa
# pylint: skip-file

import plotly.express as px
import pandas as pd
import numpy as np

def create_pollution_trend_figure_with_filters(df, selected_years, selected_pollutants):
    # Filter by selected years
    df_filtered = df[(df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])].copy()

        # Convert mg/m³ columns to μg/m³
    mg_cols = ['CO', 'CH4', 'NMHC','TCH']
    for col in mg_cols:
        if col in df_filtered.columns:
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce') * 1000  # mg → μg

    # Compute Overall Average across all pollutants (after conversion)
    pollutant_cols = [col for col in df_filtered.columns if col not in ['year', 'station', 'date']]
    df_filtered['Overall_Avg'] = df_filtered[pollutant_cols].mean(axis=1)

    # Group by year
    annual_avg = df_filtered.groupby('year')[['Overall_Avg'] + selected_pollutants].mean().reset_index()

    # Melt into long format
    melted = annual_avg.melt(id_vars='year', var_name='Pollutant', value_name='Average Concentration')

    # Compute log(1 + concentration)
    melted['Log Concentration'] = np.log1p(melted['Average Concentration'])

    # Plot on log scale but show original + log in hover
    fig = px.line(
        melted,
        x='year',
        y='Log Concentration',
        color='Pollutant',
        markers=True,
        title=f'Average Annual Pollution in Madrid (log scale) ({selected_years[0]}–{selected_years[1]})',
        hover_data={
            'year': True,
            'Pollutant': True,
            'Average Concentration': ':.2f',
            'Log Concentration': ':.2f'
        },
        custom_data=['Pollutant','Average Concentration', 'Log Concentration']
    )

    fig.update_layout(
        title = {
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title='Log(1 + Concentration, μg/m³)'
    )
    
    fig.update_traces(
        hovertemplate=(
            "<b>Year:</b> %{x}<br>"
            "<b>Pollutant:</b> %{customdata[0]}<br>"
            "<b>Average Concentration:</b> %{customdata[1]:.2f} μg/m³<br>"
            "<b>Log Concentration:</b> %{customdata[2]:.2f} μg/m³<br>"
            "<extra></extra>"
        )
    )
    
        # fig.update_layout(
        # plot_bgcolor='rgba(0,0,0,0)',  
        # paper_bgcolor='rgba(0,0,0,0)',

    return fig