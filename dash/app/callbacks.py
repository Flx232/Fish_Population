from dash import Input, Output, State, ctx
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from app.process_data import *
from app.style import *
from app.regression import create_lin_reg_plot

YEARLY_FISH = get_yearly_fish()
YEARLY_WATER = get_yearly_water()
YEARLY_SEAGRASS = get_yearly_seagrass()
YEARLY_DOCK = get_pivot_dock()
YEARLY_CARGO = get_yearly_cargo()
YEARLY_CRUISE = get_yearly_cruise()

def _empty_fig(msg):
    return go.Figure().update_layout(
        height=600,
        title=msg,
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[dict(
            text=msg, x=0.5, y=0.5, xref="paper", yref="paper",
            showarrow=False, font=dict(size=14, color="#888"),
        )],
    )
tab_values = ['title-tab', 'background-tab', 'data-source-tab', 'etl-tab', 'water-graphs', 'human-graphs', 'fish-table', 'correlation', 'time-graphs', 'reg-graphs']
def get_slide_mech(app):
    @app.callback(
        Output('main-tabs', 'value'),
        Input('prev-tab-btn', 'n_clicks'),
        Input('next-tab-btn', 'n_clicks'),
        State('main-tabs', 'value'),
        prevent_initial_call=True,
    )
    def navigate_slides(_, __, current_tab):
        if current_tab not in tab_values:
            current_tab = tab_values[0]
        current_index = tab_values.index(current_tab)
        if ctx.triggered_id == 'prev-tab-btn':
            current_index = max(0, current_index - 1)
        elif ctx.triggered_id == 'next-tab-btn':
            current_index = min(len(tab_values) - 1, current_index + 1)

        return tab_values[current_index]

    @app.callback(
        Output('prev-tab-btn', 'disabled'),
        Output('next-tab-btn', 'disabled'),
        Output('slide-indicator', 'children'),
        Input('main-tabs', 'value'),
    )
    def update_slide_controls(current_tab):
        if current_tab not in tab_values:
            current_index = 0
        else:
            current_index = tab_values.index(current_tab)

        return (
            current_index == 0,
            current_index == len(tab_values) - 1,
            f'Slide {current_index + 1} of {len(tab_values)}',
        )

def get_corr_callbacks(app):
    @app.callback(
        Output('corr-fish-water', 'figure'),
        Input('fish-dropdown-corr', 'value')
    )
    def create_fish_water_seagrass_corr(fish):
        if fish is None:
            return go.Figure()
        scientific, common = fish.split(' - ')
        fish_specific = YEARLY_FISH[YEARLY_FISH['SCIENTIFIC_NAME'] == scientific]
        fish_specific = fish_specific.drop(['MAX_SIZE', 'MIN_SIZE'], axis=1)
        aggregate_data = (fish_specific.merge(YEARLY_WATER, how='inner', on='YEAR'))
        aggregate_data = (aggregate_data.merge(YEARLY_SEAGRASS, how='inner', on='YEAR'))
        aggregate_data = aggregate_data.drop('YEAR', axis=1)
        corr_mat = aggregate_data.corr(method='spearman', numeric_only=True)
        figure=px.imshow(
            corr_mat,
            text_auto=True,
            title=f"Feature Correlation Matrix ({common}, Water Quality and Seagrass)",
            labels={"color": "Correlation"}
        ).update_layout(height=600)
        return figure

    @app.callback(
        Output('corr-fish-cargo', 'figure'),
        Input('fish-dropdown-corr', 'value')
    )
    def create_fish_cargo_corr(fish):
        if fish is None:
            return go.Figure()
        scientific, common = fish.split(' - ')
        fish_specific = YEARLY_FISH[YEARLY_FISH['SCIENTIFIC_NAME'] == scientific]
        fish_specific = fish_specific.drop(['MAX_SIZE', 'MIN_SIZE'], axis=1)
        aggregate_data = (fish_specific.merge(YEARLY_CARGO, how='inner', on='YEAR'))
        aggregate_data = (aggregate_data.merge(YEARLY_DOCK, how='inner', on='YEAR'))
        aggregate_data = (aggregate_data.merge(YEARLY_CRUISE, how='inner', on='YEAR'))
        aggregate_data = aggregate_data.drop('YEAR', axis=1)
        numeric = aggregate_data.select_dtypes('number')
        if len(aggregate_data) < 2 or numeric.shape[1] < 2:
            return _empty_fig(
                f"Not enough overlapping data for {common} "
                f"({len(aggregate_data)} rows, {numeric.shape[1]} numeric cols)"
            )
        corr_mat = aggregate_data.corr(method='spearman', numeric_only=True)
        figure=px.imshow(
            corr_mat,
            text_auto=True,
            title=f"Feature Correlation Matrix ({common}, Cargo)",
            labels={"color": "Correlation"}
        ).update_layout(height=600)
        return figure

    @app.callback(
        Output('common-name-corr', 'children'),
        Input('fish-dropdown-corr', 'value')
    )
    def get_common_fish_name_corr(fish):
        if fish is None:
            return None
        common = fish.split(' - ')[1]
        return common
    
def get_graphs_callbacks(app):
    @app.callback(
        Output('fish-water-time-graph', 'figure'),
        Input('fish-dropdown-graphs', 'value')
    )
    def create_fish_temp_graph(fish):
        if fish is None:
            return go.Figure()
        scientific, _ = fish.split(' - ')
        fish_specific = YEARLY_FISH[YEARLY_FISH['SCIENTIFIC_NAME'] == scientific]
        aggregate_data = (fish_specific.merge(YEARLY_WATER, how='inner', on='YEAR'))
        figure=px.line(
            aggregate_data,
            x = 'YEAR',
            y = ['SAMPLE_SIZE', 'WATER_TEMP'],
            title=f"Fish vs Water Temperature over Time",
        )
        return figure

    @app.callback(
        Output('fish-acre-time-graph', 'figure'),
        Input('fish-dropdown-graphs', 'value')
    )
    def create_fish_acre_graph(fish):
        if fish is None:
            return go.Figure()
        scientific, _ = fish.split(' - ')
        fish_specific = YEARLY_FISH[YEARLY_FISH['SCIENTIFIC_NAME'] == scientific]
        aggregate_data = (fish_specific.merge(YEARLY_SEAGRASS, how='inner', on='YEAR'))
        aggregate_data['ACRES (10k)'] = aggregate_data['ACRES']/10000
        figure=px.line(
            aggregate_data,
            x = 'YEAR',
            y = ['SAMPLE_SIZE', 'ACRES (10k)'],
            title=f"Fish vs Seagrass Acres over Time",
        )
        return figure

    @app.callback(
        Output('fish-revenue-graph', 'figure'),
        Input('fish-dropdown-graphs', 'value')
    )
    def create_fish_revenue_graph(fish):
        if fish is None:
            return go.Figure()
        scientific, _ = fish.split(' - ')
        fish_specific = YEARLY_FISH[YEARLY_FISH['SCIENTIFIC_NAME'] == scientific]
        aggregate_data = (fish_specific.merge(YEARLY_DOCK, how='inner', on='YEAR'))
        aggregate_data['CARGO (1 mil)'] = (aggregate_data['CARGO_Wharfage'] + aggregate_data['CARGO_Dockage'])/1000
        aggregate_data['CRUISE (1 mil)'] = (aggregate_data['CRUISE_Dockage'] + aggregate_data['CRUISE_Wharfage'])/1000
        aggregate_data['OTHER (1 mil)'] = (aggregate_data['OTHER_Dockage'] + aggregate_data['OTHER_Wharfage'])/1000
        figure=px.line(
            aggregate_data,
            x = 'YEAR',
            y = ['SAMPLE_SIZE', 'CARGO (1 mil)', 'CRUISE (1 mil)', 'OTHER (1 mil)'],
            title=f"Fish vs Tampa Bay Dock Revenue",
        )
        return figure

    @app.callback(
        Output('fish-cargo-graph', 'figure'),
        Input('fish-dropdown-graphs', 'value')
    )
    def create_fish_cargo_graph(fish):
        if fish is None:
            return go.Figure()
        scientific, _ = fish.split(' - ')
        fish_specific = YEARLY_FISH[YEARLY_FISH['SCIENTIFIC_NAME'] == scientific]
        aggregate_data = (fish_specific.merge(YEARLY_CARGO, how='inner', on='YEAR'))
        aggregate_data['DRY (100 Thou)'] = aggregate_data['DRY']/100
        aggregate_data['LIQUID (100 Thou)'] = aggregate_data['LIQUID']/100
        aggregate_data['GENERAL (100 Thou)'] = aggregate_data['GENERAL']/100
        figure=px.line(
            aggregate_data,
            x = 'YEAR',
            y = ['SAMPLE_SIZE', 'DRY (100 Thou)', 'LIQUID (100 Thou)', 'GENERAL (100 Thou)'],
            title=f"Fish vs Tampa Bay Shipping",
        )
        return figure

    @app.callback(
        Output('common-name-graphs', 'children'),
        Input('fish-dropdown-graphs', 'value')
    )
    def get_common_fish_name_graphs(fish):
        if fish is None:
            return None
        common = fish.split(' - ')[1]
        return common

def get_regr_graphs_callbacks(app):
    @app.callback(
        Output('fish-time-reg-graph', 'figure'),
        Input('fish-dropdown-reg', 'value')
    )
    def create_fish_time_reg(fish):
        if fish is None:
            return go.Figure()
        scientific, common = fish.split(' - ')
        fish_specific = YEARLY_FISH[YEARLY_FISH['SCIENTIFIC_NAME'] == scientific]
        aggregate_data = (fish_specific.merge(YEARLY_WATER, how='inner', on='YEAR'))
        features = ['YEAR']
        X = aggregate_data[features]
        y = aggregate_data['SAMPLE_SIZE']
        return create_lin_reg_plot(X, y, 'Year', f'Sample Size of {common}', 'Sample Population over Year')

    @app.callback(
        Output('common-name-reg', 'children'),
        Input('fish-dropdown-reg', 'value')
    )
    def get_common_fish_name_reg(fish):
        if fish is None:
            return None
        common = fish.split(' - ')[1]
        return common