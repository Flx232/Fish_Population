from dash import Dash, dash_table, html, dcc
import plotly.express as px
import pandas as pd
from app.process_data import *
from app.style import label_display_style
from app.general_graphs import *

yearly_fish = get_yearly_fish()
specific_fish_species = yearly_fish[~get_general_species_mask()]
unique_fish_list = (specific_fish_species['SCIENTIFIC_NAME'] + ' - ' + specific_fish_species['COMMON_NAME']).drop_duplicates().tolist()
GRAPH_LAYOUT = {'flex': '1', 'minHeight': '0', 'minWidth': '0'}
GRAPH_ROW = {'flex': '1', 'display': 'flex', 'flexDirection': 'row'}
TITLE = {'fontSize': '36px', 'textAlign': 'center'}
BACKGROUND_SIDE = {'flex': '1 1 50%', 'minWidth': '0'}

def specific_fish_dropdown(dropdown_id, label_id):
    return html.Div([
        html.Div([dcc.Dropdown(
            unique_fish_list,
            unique_fish_list[0],
            id=dropdown_id,
            clearable=False,
        )], style={"flex": "1 1 0", "minWidth": "0"}),
        html.Label(
            id = label_id,
            style=label_display_style,
        ),
    ], style={
        "display": "flex",
        "alignItems": "center",
        "gap": "12px",
        "width": "100%",
    })

title_tab = dcc.Tab(
    label="Title",
    value="title-tab",
    children = [
    html.H1("Tampa Bay Fish Sample & Environment Analysis", style={'fontSize': '46px', 'textAlign': 'center'}),
    html.H2("Frank Xu", style=TITLE),
    html.Div([
    html.Img(src='/assets/tampa_bay.png',
                style={'width': '100%', 'maxWidth': '700px', 'height': 'auto'}),
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'width': '100%',
    })
])

background_tab = dcc.Tab(
    label="Background",
    value="background-tab",
    children = [
    html.H1("Why this project?", style=TITLE),
    html.Div([
        html.P("""
            Every year, we see breaking news about how humanity's impact on the environment 
            has lead to the increasing temperatures in our waters. Scientists have pointed towards 
            increased human activities, such as increased construction and shipping, as the 
            major factor for these changes. When I was young, a book that has left the largest 
            impression on me was a visual novel detailing a marine biologist's family witnessing 
            the ocean they grew up with slowly disappear. Therefore, I want to visualize the 
            impact of Anthropomorphic climate change on the Tampa Bay region in Florida to raise 
            awareness.""", style={
                'fontSize': '24px', 
                'margin': 0,
                **BACKGROUND_SIDE,
            },
        ),
        dcc.Graph(figure=create_temp_time_graph(), style={**BACKGROUND_SIDE, 'height': '450px'},),
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'center',
        'gap': '24px',
        'width': '100%',
    }),
    html.Div([
        html.H2("""
            Hypothesis""", style={
                'fontSize': '24px', 
                'margin': 0,
                **BACKGROUND_SIDE,
            },
        ),
        html.Ul([
            html.Li("There is a direct correlation between human anthropomorphic climate change and a decline in marine life population in Tampa Bay."),
            html.Li("A growth in Sea Grass has a positive correlation with the population of marine life in the area."),
            html.Li("Increase of vessel presence leads to the decline of marine life and sea grass growth."),
            html.Li("PH Change has an impact on the amount of dissolved gasses in the water."),
            html.Li("PH and Salinity rises with the temperature of the water."),
        ], style={
                'fontSize': '24px', 
                'margin': 0,
                **BACKGROUND_SIDE,
            },
        )
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'center',
        'gap': '24px',
        'width': '100%',
    }),
])

data_source_tab = dcc.Tab(
    label="Data Source",
    value="data-source-tab",
    children = [
    html.H1("What data is used? How is it used?", style=TITLE),
    html.P("""
        The data used in this project was graciously sourced from the Tampa Port Authority, 
        Tampa Bay Estuary Program, Sarasota County Water Atlas, and the Florida Fish and 
        Wildlife Conservation Commission. The data itself consisted of thousands of rows and 
        required prior cleaning using Excel for some of the data. For others, I had to 
        manually write down key data from a report. An important note is that the Florida 
        Fish and wildlife Conservation Commission's website states that the sampling recorded 
        in the data can be used to extrapolate to the fish population as a whole. Therefore I 
        took great liberty in treating the sample size as a proxy for the population size. 
        However, we must keep in mind that the trends may not be entirely accurate.""", style={'fontSize': '24px'}),
    html.Div([
        dcc.Graph(figure=create_agg_fish_temp_time_graph(), style=GRAPH_LAYOUT),
        dcc.Graph(figure=create_agg_fish_seagrass_time_graph(), style=GRAPH_LAYOUT),
    ], style=GRAPH_ROW),
])

etl_tab = dcc.Tab(
    label="ETL Process",
    value="etl-tab",
    children = [
    html.H1("ETL Process", style=TITLE),
    html.P("""The ETL process did not require much due to already processing the data using Excel 
    power queries. However, I still needed to transform and load the data. The tools I use are PySpark, 
    Apache Airflow, and Snowflake. I used PySpark due to how quickly it can process the data through parallelization 
    using clustering computing. I picked Airflow due to how easily I can create a pipeline using direct acyclic graphs 
    to run multiple processes in parallel. Finally, I use snowflake as an experimentation with cloud computing.""",
    style={'fontSize': '24px'}),
    html.Div([
        html.Img(
            src='/assets/pyspark.png', 
            style={'width': '100%', 'maxWidth': '250px', 'height': 'auto', 'borderRadius': '8px'}
        ),
        html.Img(
            src='/assets/airflow.png', 
            style={'width': '100%', 'maxWidth': '250px', 'height': 'auto', 'borderRadius': '8px'}
        ),
        html.Img(
            src='/assets/snowflake.png', 
            style={'width': '100%', 'maxWidth': '250px', 'height': 'auto', 'borderRadius': '8px'}
        ),
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'justifyContent': 'center',
        'alignItems': 'center',
        'gap': '20px',
        'flexWrap': 'wrap',
        'width': '100%',
        'margin': '20px 0',
    }),
    html.Div([
        html.Img(
            src='/assets/dag.png',
            style={'width': '100%', 'maxWidth': '700px', 'height': 'auto', 'borderRadius': '8px'}
        )
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'width': '100%',
        'marginTop': '20px'
    })
])

water_feature_relations = dcc.Tab(
    label="Water Quality",
    value="water-graphs",
    children = [
    html.H1("Water Quality Graphs", style=TITLE),
    html.Div([
        html.Div([
            dcc.Graph(figure=create_temp_salinity_graph(), style=GRAPH_LAYOUT),
            dcc.Graph(figure=create_ph_ammonia_graph(), style=GRAPH_LAYOUT),
        ], style=GRAPH_ROW),
    ]),
])

cargo_feature_relations = dcc.Tab(
    label="Human Impact",
    value="human-graphs",
    children = [
    html.H1("Shipping Impact Graphs", style=TITLE),
    html.Div([
        html.Div([
            dcc.Graph(figure=create_revenue_impact_graph(), style=GRAPH_LAYOUT),
            dcc.Graph(figure=create_land_use_impact_graph(), style=GRAPH_LAYOUT),
            dcc.Graph(figure=create_shipping_content_graph(), style=GRAPH_LAYOUT),
        ], style=GRAPH_ROW),
    ]),
])

featured_fish_tab = dcc.Tab(
    label="Featured Fish",
    value="fish-table",
    children = [
    html.H1("Fish Featured in the Following Slides:", style=TITLE),
    dash_table.DataTable(
        yearly_fish.groupby(['SCIENTIFIC_NAME', 'COMMON_NAME'], as_index=False)['SAMPLE_SIZE'].sum().astype({'SAMPLE_SIZE': int}).to_dict("records"),
        page_size=15, sort_action="native",
        style_table={'overflowX': 'scroll'},
    )
])

time_graphs_tab = dcc.Tab(
    label="Fish Over Time",
    value="time-graphs",
    children = [
    html.H1("Fish samples and Features in relation to time", style={'textAlign': 'center'}),
    specific_fish_dropdown('fish-dropdown-graphs', 'common-name-graphs'),
    html.Div([
        html.Div([
            dcc.Graph(id='fish-water-time-graph', style=GRAPH_LAYOUT),
            dcc.Graph(id='fish-acre-time-graph', style=GRAPH_LAYOUT),
        ], style=GRAPH_ROW),
        html.Div([
            dcc.Graph(id='fish-revenue-graph', style=GRAPH_LAYOUT),
            dcc.Graph(id='fish-cargo-graph', style=GRAPH_LAYOUT),
        ], style=GRAPH_ROW),
    ]),
])

regression_graphs_tab = dcc.Tab(
    label="Fish Regression",
    value="reg-graphs",
    children = [
    html.H1("Regression Graphs", style={'textAlign': 'center'}),
    specific_fish_dropdown('fish-dropdown-reg', 'common-name-reg'),
    html.Div([
        html.Div([
            dcc.Graph(figure=create_total_fish_time_reg(), style=GRAPH_LAYOUT),
            dcc.Graph(figure=create_temp_time_reg(), style=GRAPH_LAYOUT),
            dcc.Graph(id='fish-time-reg-graph', style=GRAPH_LAYOUT),
        ], style=GRAPH_ROW),
    ]),
])

correlation_tab = dcc.Tab(
    label="Correlation Matrix",
    value="correlation",
    children = [
    html.Div([
        html.H1("Correlation Matrices between sample sizes and other features", style={'textAlign': 'center'}),
        specific_fish_dropdown('fish-dropdown-corr', 'common-name-corr'),
        html.Div([
            dcc.Graph(id='corr-fish-water', style=GRAPH_LAYOUT),
            dcc.Graph(id='corr-fish-cargo', style=GRAPH_LAYOUT),
        ], style=GRAPH_ROW),
        html.Div([
            dcc.Graph(figure=create_fish_water_seagrass_corr(), style=GRAPH_LAYOUT),
            dcc.Graph(figure=create_fish_cargo_corr(), style=GRAPH_LAYOUT),
        ], style=GRAPH_ROW),
    ]),
])