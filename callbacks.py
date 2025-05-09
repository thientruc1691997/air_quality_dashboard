# flake8: noqa

from dash import Input, Output
from plot_line_chart import create_pollution_trend_figure_with_filters

def register_callbacks(app, combined_df):
    @app.callback(
        Output('pollution-line-plot', 'figure'),
        Input('year-range-slider', 'value'),
        Input('pollutant-dropdown', 'value')
    )
    def update_line_chart(selected_years, selected_pollutants):
        if not selected_pollutants:
            return {
                'data': [],
                'layout': {'title': 'Please select at least one pollutant.'}
            }

        fig = create_pollution_trend_figure_with_filters(
            combined_df, selected_years, selected_pollutants
        )
        return fig