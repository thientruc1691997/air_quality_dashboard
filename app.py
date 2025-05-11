# flake8: noqa

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from layout import create_layout, create_mainpage
from callbacks import register_callbacks, register_page_callbacks
from data_loader import load_pollution_data, load_station_metadata
import pandas as pd
import os


# Load all data once and share across components
base_path = '/Users/nguyentruc/Desktop/UHasselt/Data Visualization/Project/VDS2425_Madrid/Dashboard/data'
years = range(2001, 2019)
dfs = []

for year in years:
    file_path = os.path.join(base_path, f'madrid_{year}.parquet')  # Changed from .csv to .parquet
    df_year = load_pollution_data(file_path)
    df_year['year'] = year
    dfs.append(df_year)

combined_df = pd.concat(dfs, ignore_index=True)
stations_df = load_station_metadata(os.path.join(base_path, 'stations.parquet'))  # Changed from .csv to .parquet

def load_data():
    data_path = os.path.join(
        os.path.dirname(__file__), 
        "data/compressed_data.parquet.gzip"
    )
    return pd.read_parquet(data_path)    

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP, 
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
        ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    suppress_callback_exceptions=True
)

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/brPBPO.css'  # Dash core CSS
})

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