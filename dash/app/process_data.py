from app.api import *
import pandas as pd

def yearify_date(data, agg_columns, numeric_columns):
    data = data.set_index('DATE').sort_index()
    yearly_avg = data.groupby(agg_columns).resample('YE').agg({
        col: 'mean' for col in numeric_columns
    }).reset_index()
    yearly_avg['YEAR'] = yearly_avg['DATE'].dt.year
    return yearly_avg

def get_yearly_fish():
    agg_columns = ['SCIENTIFIC_NAME', 'COMMON_NAME']
    numeric_columns = ['SAMPLE_SIZE', 'AVG_SIZE', 'MAX_SIZE', 'MIN_SIZE']
    fish_data = get_fish_data()
    fish_data = fish_data.dropna(subset=['SAMPLE_SIZE'])
    yearly_fish = yearify_date(fish_data, agg_columns, numeric_columns).dropna()
    counts = yearly_fish.groupby(agg_columns)['SCIENTIFIC_NAME'].transform('size')
    filtered_fish = yearly_fish[counts > 10]
    return filtered_fish

def get_yearly_water():
    agg_columns = ['REGION_NAME']
    numeric_columns = ['NH3_N_MGL', 'PH', 'SALINITY', 'WATER_TEMP']
    water_data = get_water_quality_data()
    yearly_water = yearify_date(water_data, agg_columns, numeric_columns).dropna()
    return yearly_water

def get_pivot_dock():
    dock_revenue = get_dock_data()
    dock_revenue = dock_revenue.set_index(['YEAR','TYPE'])[['CARGO','CRUISE','OTHER']].unstack('TYPE').reset_index()
    dock_revenue.columns = [f'{m}_{t}' if t else m for m, t in dock_revenue.columns]
    return dock_revenue

def get_yearly_seagrass():
    seagrass_data = get_seagrass_data()
    yearly_acrage = seagrass_data.groupby('YEAR')[['ACRES']].sum().reset_index()
    return yearly_acrage

def get_general_species_mask():
    fish = get_yearly_fish()
    mask = fish['SCIENTIFIC_NAME'].str.contains('spp.')
    return mask

def get_yearly_cruise():
    return get_cruise_data()

def get_yearly_cargo():
    return get_shipment_data()

def get_yearly_revenue():
    return get_region_revenue_data()
