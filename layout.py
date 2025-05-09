# flake8: noqa
# pylint: skip-file

import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html
from data_preprocess import compute_station_averages
from plot_station_map import create_station_map_figure_with_custom_hover
from plot_change_map import create_station_change_bar_figure


def create_layout(app, combined_df, stations_df):
    common_pollutants = ['BEN', 'CO', 'EBE', 'NMHC', 'NO_2', 'O_3', 'PM10', 'SO_2', 'TCH', 'TOL']

    return dbc.Container(
        fluid=True,
        className='dashboard-container',
        style={'padding': '0', 'margin': '0', 'height': '100vh', 'overflow': 'hidden'},
        children=[
            dbc.Row(
                [
                    # Left sidebar column
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H1(
                                        [
                                            html.Span("Welcome"),
                                            html.Br(),
                                            html.Span("to Group 4 dashboard!")
                                        ],
                                        className='sidebar-title'
                                    ),
                                    html.P(
                                        "This dashboard shows air pollution trends and station changes in Madrid.",
                                        className='sidebar-text'
                                    ),
                                    html.Hr(className='sidebar-divider'),
                                    html.P("Explore the sections on the right:", className='sidebar-text'),
                                    html.Ul(
                                        [
                                            html.Li("Annual pollution trends (2001–2018)", className='sidebar-item'),
                                            html.Li("Station-wise pollution map for 2018", className='sidebar-item'),
                                            html.Li("Station pollution change between 2008 and 2018", className='sidebar-item')
                                        ],
                                        className='sidebar-list'
                                    )
                                ],
                                className='sidebar',
                                style={
                                    "height": "100vh",
                                    "padding": "2rem",
                                    "backgroundColor": "#1f2c56",
                                    "color": "white",
                                    "overflowY": "auto"
                                }
                            )
                        ],
                        width=3,
                        style={'padding': '0'}
                    ),

                    # Right content column
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    # Section 1: Annual Pollution Trends
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(html.H3('1. Annual Pollution Trends (2001–2018)', className='section-title')),
                                            dbc.CardBody(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                [
                                                                    html.Label('Select Year Range:', className='control-label'),
                                                                    dcc.RangeSlider(
                                                                        id='year-range-slider',
                                                                        min=2001,
                                                                        max=2018,
                                                                        step=1,
                                                                        marks={year: str(year) for year in range(2001, 2019)},
                                                                        value=[2001, 2018],
                                                                        className='year-slider'
                                                                    )
                                                                ],
                                                                width=12,
                                                                className='mb-3'
                                                            ),
                                                            dbc.Col(
                                                                [
                                                                    html.Label('Select Pollutants:', className='control-label'),
                                                                    dcc.Dropdown(
                                                                        id='pollutant-dropdown',
                                                                        options=[{'label': p, 'value': p} for p in common_pollutants],
                                                                        value=common_pollutants,
                                                                        multi=True,
                                                                        className='pollutant-dropdown'
                                                                    )
                                                                ],
                                                                width=12
                                                            )
                                                        ]
                                                    ),
                                                    dcc.Graph(
                                                        id='pollution-line-plot',
                                                        style={'height': '400px'},
                                                        className='plot-container'
                                                    )
                                                ],
                                                className='section-content'
                                            )
                                        ],
                                        className='mb-4 section-card'
                                    ),

                                    # Section 2: Station-wise Pollution Map
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(html.H3('2. Station-wise Pollution Map (2018)', className='section-title')),
                                            dbc.CardBody(
                                                [
                                                    dcc.Graph(
                                                        id='station-map',
                                                        figure=create_station_map_figure_with_custom_hover(combined_df, stations_df),
                                                        style={'height': '600px'},
                                                        className='plot-container'
                                                    )
                                                ],
                                                className='section-content'
                                            )
                                        ],
                                        className='mb-4 section-card'
                                    ),

                                    # Section 3: Station Change
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(html.H3('3. Station Change Between 2008 and 2018', className='section-title')),
                                            dbc.CardBody(
                                                [
                                                    dcc.Graph(
                                                        id='station-change-bar',
                                                        figure=create_station_change_bar_figure(combined_df, stations_df),
                                                        style={'height': '500px'},
                                                        className='plot-container'
                                                    )
                                                ],
                                                className='section-content'
                                            )
                                        ],
                                        className='section-card'
                                    )
                                ],
                                style={
                                    'height': '100vh',
                                    'overflowY': 'auto',
                                    'padding': '2rem',
                                    'backgroundColor': '#f8f9fa'
                                }
                            )
                        ],
                        width=9,
                        style={'padding': '0'}
                    )
                ],
                style={'margin': '0', 'height': '100vh'}
            )
        ]
    )