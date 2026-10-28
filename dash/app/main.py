from dash import Dash, dash_table, html, dcc
import plotly.express as px
import pandas as pd
from pathlib import Path
from app.callbacks import *
from app.style import *
from app.tabs import *

app = Dash()
app.layout = [
    html.Section([
        dcc.Store(id='selected-country', data=None),
        html.Div([
            dcc.Tabs(
                [title_tab, background_tab, data_source_tab, 
                 etl_tab, water_feature_relations, cargo_feature_relations, 
                 featured_fish_tab, correlation_tab, time_graphs_tab, 
                 regression_graphs_tab, conclusion_tab, work_cited_tab],
                id='main-tabs',
                value='title-tab',
                style={'display': 'none'}
            ),
        ]),
        html.Div([
            html.Button(
                '❮ Previous',
                id='prev-tab-btn',
                n_clicks=0,
                style=base_btn_style,
            ),
            html.Div(
                id='slide-indicator',
                children='Slide 1 of 3',
                style={'fontSize': '14px', 'fontWeight': '600', 'color': '#475569'},
            ),
            html.Button(
                'Next ❯',
                id='next-tab-btn',
                n_clicks=0,
                style=base_btn_style,
            ),
        ], style=footer_style),
    ], style={'padding': '2rem 2rem 6rem', 'background_color': "#EAE7E0"})
]
get_slide_mech(app)
get_corr_callbacks(app)
get_graphs_callbacks(app)
get_regr_graphs_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)