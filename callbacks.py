# flake8: noqa

from dash import Input, Output
from plot_line_chart import create_pollution_trend_figure_with_filters
from layout import create_mainpage, create_layout

def register_callbacks(app, combined_df):
    @app.callback(
        Output('pollution-line-plot', 'figure'),
        Input('year-range-slider', 'value'),
        Input('pollutant-dropdown', 'value')
    )
    def update_line_chart(selected_years, selected_pollutants):
        # Even if no pollutants are selected, still return the animated overall line
        fig = create_pollution_trend_figure_with_filters(
            combined_df, selected_years, selected_pollutants
        )
        return fig

def register_page_callbacks(app, combined_df, stations_df):
    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        # Default to main page if no pathname or root path
        if pathname is None or pathname == '/':
            return create_mainpage(app, combined_df, stations_df)
        elif pathname == '/detail':
            return create_layout(app, combined_df, stations_df)
        else:
            # Optional: add 404 handling or redirect to main page
            return create_mainpage(app, combined_df, stations_df)