from app.snowflake_engine import query

def get_seagrass_data():
    statement = """
    select r.name as region_name, w.name as water_body_name, acres, year
    from seagrass g join water w on g.water_id = w.water_id
    join region r on r.region_id = w.region_id;
    """
    return query(statement)

def get_fish_data():
    statement = """
    select common_name, scientific_name, name as region_name, 
    avg_size, max_size, min_size, sample_size, date
    from fish_data fd join fish f on fd.fish_id = f.fish_id
    join region r on fd.region_id = r.region_id;
    """
    return query(statement)

def get_water_quality_data():
    statement = """
    select r.name as region_name, w.name as water_body_name, nh3_n_mgl, ph, 
    salinity, water_temp, date
    from water_quality wq join water w on wq.water_id = w.water_id
    join region r on r.region_id = w.region_id;
    """
    return query(statement)

def get_shipment_data():
    statement = """
    select r.name as region_name, dry, general, liquid, car.year
    from cargo car join region_revenue rr on rr.region_id = car.region_id
    join region r on r.region_id = rr.region_id;
    """
    return query(statement)

def get_cruise_data():
    statement = """
    select r.name as region_name, revenue as CRUISE_REVENUE, cru.year
    from cruise cru join region r on r.region_id = cru.region_id;
    """
    return query(statement)

def get_region_revenue_data():
    statement = """
    select r.name as region_name, land_lease, net_investment, port_usage_fee, rr.year
    from region_revenue rr join region r on r.region_id = rr.region_id;
    """
    return query(statement)

def get_dock_data():
    statement = """
    select r.name as region_name, cargo, cruise, other, type, dr.year
    from dock_revenue dr 
    join dock_type dt on dr.dock_type_id = dt.dock_type_id
    join region r on dr.region_id = r.region_id;
    """
    return query(statement)