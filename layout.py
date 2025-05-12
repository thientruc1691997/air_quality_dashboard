# flake8: noqa
# pylint: skip-file
# type: ignore

import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html
from data_preprocess import compute_station_averages
from plot_station_map import create_station_map_figure_with_custom_hover
from plot_change_map import create_station_change_bar_figure
from main_page_plot import create_pollutant_barchart, create_main_map


def create_layout(app, combined_df, stations_df):
    common_pollutants = ['BEN', 'CO', 'EBE', 'NMHC', 'NO_2', 'O_3', 'PM10', 'SO_2', 'TCH', 'TOL']

    return dbc.Container(
        fluid=True,
        className='dashboard-container',
        style={'padding': '0', 'margin': '0', 'height': '100vh', 'overflow': 'hidden'},
        children=[
            dbc.Row(
                [
                    # Left sidebar
                    dbc.Col(
                        [
                            html.Div(
                                [   
                                    dbc.Button(
                                        html.I(className="fa fa-arrow-circle-left"),
                                        href="/",
                                        id="back-to-main-button",
                                        style={
                                            'fontSize': '24px',
                                            'color': 'white',
                                            'background': 'none',
                                            'border': 'none',
                                            'padding': '0',
                                            'marginBottom': '15px',
                                            'cursor': 'pointer',
                                            'transition': 'all 0.3s ease'
                                            },
                                            className="back-button"
                                        ),
                                    html.H1(
                                        [
                                            html.Span("Group 4")
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
                                            html.Li(
                                                html.A("How has pollution in Madrid evolved between 2001 and 2018?", href="#section-1", className='sidebar-link'),
                                                className='sidebar-item'
                                            ),
                                            html.Li(
                                                html.A("Which are the areas of Madrid where pollution is highest / lowest in 2018?", href="#section-2", className='sidebar-link'),
                                                className='sidebar-item'
                                            ),
                                            html.Li(
                                                html.A("Which are the areas of Madrid where pollution has improved / worsened more between 2008 and 2018?", href="#section-3", className='sidebar-link'),
                                                className='sidebar-item'
                                            ), 
                                            html.Li(
                                                html.A("How have the different measurements of pollution evolved between 2008 and 2018?", href="#section-1", className='sidebar-link'),
                                                className='sidebar-item'
                                            )
                                        ],
                                        className='sidebar-list'
                                    )
                                ],
                                className='sidebar',
                                style={
                                    "height": "100vh",
                                    "padding": "2rem",
                                    'background': 'linear-gradient(to right, #FED8F7 0%, #C4DDFE 100%)',
                                    "color": "#7f8a9c",
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
                                    # Section 1
                                    html.Div(id='section-1'),  # anchor
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
                                                                        value=[],
                                                                        multi=True,
                                                                        placeholder = "select pollutants to display",
                                                                        className='pollutant-dropdown'
                                                                    )
                                                                ],
                                                                width=12
                                                            )
                                                        ]
                                                    ),
                                                    dcc.Graph(
                                                        id='pollution-line-plot',
                                                        style={'height': '500px'},
                                                        className='plot-container'
                                                    )
                                                ],
                                                className='section-content'
                                            )
                                        ],
                                        className='mb-4 section-card'
                                    ),

                                    # Section 2
                                    html.Div(id='section-2'),
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(html.H3('2. Pollution Map by Stations (2018)', className='section-title')),
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

                                    # Section 3
                                    html.Div(id='section-3'),
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(html.H3('3. Pollution Change Between 2008 and 2018 by Stations', className='section-title')),
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
                                    'backgroundColor': 'rgba(0, 0, 0, 0)',
                                    'scrollBehavior': 'smooth'  # enables smooth scrolling!
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

def create_mainpage(app, combined_df, stations_df):
    # Get latest update time
    latest_date = pd.to_datetime(combined_df['date']).max()
    latest_str = latest_date.strftime('%d/%m/%Y %H:%M')
    
    # Create figures
    bar_fig = create_pollutant_barchart(combined_df)
    map_fig = create_main_map(combined_df, stations_df)

    return dbc.Container(
        fluid=True,  
        style={'backgroundColor': '#f8f9fa', 'padding': '0', 'margin': '0', 'height': '100vh', 'overflow': 'hidden'},
        children=[
            # Header
            dbc.Navbar(
                [
                    dbc.Container(
                        [
                            html.H1("Welcome to Group 4 Dashboard", 
                                style={
                                    'color': '#7f8a9c',  # Dark text for light background
                                    'margin': '10px',
                                    # 'textShadow': '0 1px 1px rgba(255,255,255,0.5)',
                                    'font-family': 'Tahoma'
                                    }),
                            dbc.Button(
                                html.I(
                                    className="fa fa-arrow-circle-right"),
                                    href="/detail",
                                    color="white", 
                                    style={
                                        'fontSize': '35px',
                                        'color': 'white',
                                        'cursor': 'pointer',
                                        'marginLeft': 'auto',
                                        'marginRight': '10px',
                                        'background': 'none',
                                        'border': 'none',
                                        'padding': '0',
                                        'transition': 'all 0.3s ease',  # Smooth transition
                                        'transform': 'scale(1)',  # Base state
                                        'opacity': '0.9'  # Slightly transparent by default
                                    },
                                    className="p-0 smooth-arrow"
                            )
                        ],
                        fluid=True,
                        style={'display': 'flex', 'alignItems': 'center'}
                    )
                ],
                style={
                    'background': 'linear-gradient(to right, #FED8F7 0%, #C4DDFE 100%)', #linear-gradient(135deg, #175491 0%, #0d355f 100%)
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
                    'padding': '15px 0'
                },
                dark=True,  # Must set to False for light background
                className="mb-4"  # Added margin bottom
            ),
            
            # Update time
            dbc.Row(
                dbc.Col(
                    html.P(f"Updated: {latest_str}", 
                          className="text-muted mb-2 mt-2",
                          style={'paddingLeft': '1rem', 'color':'#7f8a9c'}
                        ),
                    width=12   
                    )     
                ),       
            # Main content
            dbc.Row([
                # Left column - Bar chart (wider)
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4("Average Pollutant Levels in 2018", 
                                           className="mb-0"),
                                style = {
                                    'background': 'linear-gradient(to right, #CEDBFB 0%, #F8DBF6 100%)',
                                    'color': '#7f8a9c'
                                }                                    
                                ),

                                dbc.CardBody(
                                    [
                                        dcc.Graph(
                                            figure=bar_fig,
                                            config={'displayModeBar': False},
                                            style={'height': '500px', 'background': 'rgba(0,0,0,0)', 'padding':'0','border':'none'}
                                        ),
                                    ]
                                )
                            ],
                            className="h-100",
                            style={
                                'background': 'linear-gradient(to right, #CEDBFB 0%, #F8DBF6 100%)'
                            }
                        )
                    ],
                    md=6,  # Wider column for chart
                    style={'paddingRight': '10px', 'background': 'transparent'}
                ),
                
                # Right column - Map (narrower)
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4("Station Pollution Map 2018", 
                                           className="mb-0"),
                                style = {
                                    'background': 'linear-gradient(to left, #CEDBFB 0%, #F8DBF6 100%)',
                                    'color': '#7f8a9c'
                                }                                   
                                ),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(
                                            figure=map_fig,
                                            config={'displayModeBar': False},
                                            style={'height': '500px'}
                                        )
                                    ]
                                )
                            ],
                            className="h-100",
                            style={
                                'background': 'linear-gradient(to left, #CEDBFB 0%, #F8DBF6 100%)'
                            }                                                      
                        )
                    ],
                    md=6,
                    style = {
                        'paddingBottom':'0px'
                    }
                )
            ], 
            className="g-3 mx-0",  # Add gutter spacing
            style={'height': 'calc(50vh - 50px)', 'margin': '0'}
            )
        ]
    )