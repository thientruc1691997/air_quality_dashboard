# flake8: noqa

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from layout import create_layout, create_mainpage
from callbacks import register_callbacks, register_page_callbacks
from data_loader import load_pollution_data, load_station_metadata
import pandas as pd
import os


# Load all data once and share across components
base_path = '/Users/nguyentruc/Desktop/UHasselt/Data Visualization/Project/VDS2425_Madrid/'
years = range(2001, 2019)
dfs = []

for year in years:
    file_path = os.path.join(base_path, f'madrid_{year}.csv')
    df_year = load_pollution_data(file_path)
    df_year['year'] = year
    dfs.append(df_year)

combined_df = pd.concat(dfs, ignore_index=True)
stations_df = load_station_metadata(os.path.join(base_path, 'stations.csv'))


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    suppress_callback_exceptions=True
)
# Choose which layout to load (main line chart or station map)
# Comment/uncomment as needed

# Set the basic layout with navigation container
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')  # This will show either main or detail page
])
# Register callbacks
register_page_callbacks(app, combined_df, stations_df)
register_callbacks(app, combined_df)

if __name__ == '__main__':
    app.run(debug=True)
