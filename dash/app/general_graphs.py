from dash import Input, Output, State, ctx
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from app.process_data import *
from app.regression import create_lin_reg_plot

YEARLY_FISH = get_yearly_fish()[~get_general_species_mask()]
YEARLY_WATER = get_yearly_water()
YEARLY_SEAGRASS = get_yearly_seagrass()
YEARLY_DOCK = get_pivot_dock()
YEARLY_CARGO = get_yearly_cargo()
YEARLY_CRUISE = get_yearly_cruise()
YEARLY_REVENUE = get_yearly_revenue()

def create_temp_time_graph():
    figure=px.line(
        YEARLY_WATER,
        x = 'YEAR',
        y = ['WATER_TEMP'],
        title=f"Temp vs Time",
    )
    return figure

def create_agg_fish_temp_time_graph():
    aggregate_fish = YEARLY_FISH.groupby('YEAR', as_index=False)['SAMPLE_SIZE'].sum()
    aggregate_data = (aggregate_fish.merge(YEARLY_WATER, how='inner', on='YEAR'))
    aggregate_data['SAMPLE_SIZE'] = aggregate_data['SAMPLE_SIZE']/100
    figure=px.line(
        aggregate_data,
        x = 'YEAR',
        y = ['SAMPLE_SIZE', 'WATER_TEMP'],
        title=f"Total Marine Life Sample Size (100s) and Water Temp (F) vs Time",
    )
    return figure

def create_agg_fish_seagrass_time_graph():
    aggregate_fish = YEARLY_FISH.groupby('YEAR', as_index=False)['SAMPLE_SIZE'].sum()
    aggregate_data = (aggregate_fish.merge(YEARLY_SEAGRASS, how='inner', on='YEAR'))
    aggregate_data['ACRES'] = aggregate_data['ACRES']/10
    figure=px.line(
        aggregate_data,
        x = 'YEAR',
        y = ['SAMPLE_SIZE', 'ACRES'],
        title=f"Total Marine Life Sample Size and Seagrass Coverage (10s Acres) vs Time",
    )
    return figure

def create_temp_salinity_graph():
    scaled_water = YEARLY_WATER[['YEAR', 'PH', 'SALINITY', 'WATER_TEMP']]
    scaled_water['WATER_TEMP_10F'] = scaled_water['WATER_TEMP']/10
    scaled_water['SALINITY_pptt'] = scaled_water['SALINITY']/10
    figure=px.line(
        scaled_water,
        x = 'YEAR',
        y = ['PH', 'SALINITY_pptt', 'WATER_TEMP_10F'],
        title=f"Ph, Temp (10 F) and Salinity (pptt) vs Time",
    )
    return figure

def create_ph_ammonia_graph():
    chemical_water = YEARLY_WATER[['YEAR', 'PH', 'NH3_N_MGL']]
    chemical_water['NH3_N_10MUGL'] = chemical_water['NH3_N_MGL'] * 100
    figure=px.line(
        chemical_water,
        x = 'YEAR',
        y = ['PH', 'NH3_N_10MUGL'],
        title=f"Ph and NH3_N(10 µgl) vs Time",
    )
    return figure

def create_revenue_impact_graph():
    aggregate_fish = YEARLY_FISH.groupby('YEAR', as_index=False)['SAMPLE_SIZE'].sum()
    aggregate_data = (aggregate_fish.merge(YEARLY_DOCK, how='inner', on='YEAR'))
    aggregate_data['CARGO (10 thou)'] = (aggregate_data['CARGO_Wharfage'] + aggregate_data['CARGO_Dockage'])/10
    aggregate_data['CRUISE (10 thou)'] = (aggregate_data['CRUISE_Dockage'] + aggregate_data['CRUISE_Wharfage'])/10
    aggregate_data['OTHER (10 thou)'] = (aggregate_data['OTHER_Dockage'] + aggregate_data['OTHER_Wharfage'])/10
    aggregate_data['TOTAL REVENUE (10 thou)'] = aggregate_data['CARGO (10 thou)'] + aggregate_data['CRUISE (10 thou)'] + aggregate_data['OTHER (10 thou)']
    aggregate_data = aggregate_data.merge(YEARLY_SEAGRASS, how='inner', on='YEAR')
    aggregate_data['ACRES'] = aggregate_data['ACRES']/10
    figure=px.line(
        aggregate_data,
        x = 'YEAR',
        y = ['SAMPLE_SIZE', 'ACRES', 'TOTAL REVENUE (10 thou)'],
        title=f"Revenue ($10,000s), Sample size,<br>and Seagrass coverage (10s Acres) vs Time",
    )
    return figure

def create_land_use_impact_graph():
    aggregate_fish = YEARLY_FISH.groupby('YEAR', as_index=False)['SAMPLE_SIZE'].sum()
    aggregate_data = (aggregate_fish.merge(YEARLY_REVENUE, how='inner', on='YEAR'))
    aggregate_data['LAND_LEASE (10 thou)'] = (aggregate_data['LAND_LEASE'])/10
    aggregate_data = aggregate_data.merge(YEARLY_SEAGRASS, how='inner', on='YEAR')
    aggregate_data['ACRES'] = aggregate_data['ACRES']/10
    figure=px.line(
        aggregate_data,
        x = 'YEAR',
        y = ['SAMPLE_SIZE', 'ACRES', 'LAND_LEASE (10 thou)'],
        title=f"Land Lease ($10,000s), Sample size,<br>and Seagrass coverage (10s Acres) vs Time",
    )
    return figure

def create_shipping_content_graph():
    aggregate_fish = YEARLY_FISH.groupby('YEAR', as_index=False)['SAMPLE_SIZE'].sum()
    aggregate_data = (aggregate_fish.merge(YEARLY_CARGO, how='inner', on='YEAR'))
    aggregate_data['TOTAL CARGO'] = (aggregate_data['DRY'] + aggregate_data['LIQUID'] + aggregate_data['GENERAL'])/10
    aggregate_data = aggregate_data.merge(YEARLY_SEAGRASS, how='inner', on='YEAR')
    aggregate_data['ACRES'] = aggregate_data['ACRES']/10
    figure=px.line(
        aggregate_data,
        x = 'YEAR',
        y = ['SAMPLE_SIZE', 'ACRES', 'TOTAL CARGO'],
        title=f"Cargo (10,000s Tons), Sample size,<br>and Seagrass coverage (10s Acres) vs Time",
    )
    return figure

def create_fish_water_seagrass_corr():
    aggregate_fish = YEARLY_FISH.groupby('YEAR', as_index=False)['SAMPLE_SIZE'].sum()
    aggregate_data = (aggregate_fish.merge(YEARLY_WATER, how='inner', on='YEAR'))
    aggregate_data = (aggregate_data.merge(YEARLY_SEAGRASS, how='inner', on='YEAR'))
    aggregate_data = aggregate_data.drop('YEAR', axis=1)
    corr_mat = aggregate_data.corr(method='spearman', numeric_only=True)
    figure=px.imshow(
        corr_mat,
        text_auto=True,
        title=f"Feature Correlation Matrix (All Fish - Water Quality and Seagrass)",
        labels={"color": "Correlation"}
    ).update_layout(height=600)
    return figure


def create_fish_cargo_corr():
    aggregate_fish = YEARLY_FISH.groupby('YEAR', as_index=False)['SAMPLE_SIZE'].sum()
    aggregate_data = (aggregate_fish.merge(YEARLY_CARGO, how='inner', on='YEAR'))
    aggregate_data = (aggregate_data.merge(YEARLY_DOCK, how='inner', on='YEAR'))
    aggregate_data = aggregate_data.drop('YEAR', axis=1)
    corr_mat = aggregate_data.corr(method='spearman', numeric_only=True)
    figure=px.imshow(
        corr_mat,
        text_auto=True,
        title=f"Feature Correlation Matrix (All Fish - Cargo)",
        labels={"color": "Correlation"}
    ).update_layout(height=600)
    return figure

def create_total_fish_time_reg():
    aggregate_fish = YEARLY_FISH.groupby('YEAR', as_index=False)['SAMPLE_SIZE'].sum()
    aggregate_data = (aggregate_fish.merge(YEARLY_WATER, how='inner', on='YEAR'))
    features = ['YEAR']
    X = aggregate_data[features]
    y = aggregate_data['SAMPLE_SIZE']
    return create_lin_reg_plot(X, y, 'Year', f'Sample Size', 'Total Sampled Population over Year')

def create_temp_time_reg():
    features = ['YEAR']
    X = YEARLY_WATER[features]
    y = YEARLY_WATER['WATER_TEMP']
    return create_lin_reg_plot(X, y, 'Year', 'Water Temp (F)', 'Water Temperature over Year')