use role sysadmin;
use warehouse COMPUTE_WH;
use database FLORIDA_DB;
use schema water_quality_fisheries;

create or replace table region (
    region_id int autoincrement primary key,
    name varchar(128)
);

create or replace table dock_type (
    dock_type_id int autoincrement primary key,
    type varchar(128)
);

create or replace table fish (
    fish_id int autoincrement primary key,
    common_name varchar(128),
    scientific_name varchar(128)
);

create or replace table water (
    water_id int autoincrement primary key,
    region_id int references region(region_id),
    name varchar(128)
);

create or replace table seagrass (
    water_id int references water(water_id),
    acres number,
    year int
);

create or replace table region_revenue (
    region_id int references region(region_id),
    net_investment number,
    port_usage_fee number,
    land_lease number,
    year int
);

create or replace table dock_revenue (
    region_id int references region(region_id),
    cargo number,
    cruise number,
    other number,
    dock_type_id int references dock_type(dock_type_id),
    year int
);

create or replace table cargo (
    region_id int references region(region_id),
    dry number,
    liquid number,
    general number,
    year int
);

create or replace table cruise (
    region_id int references region(region_id),
    passenger_count int,
    revenue number,
    year int
);

create or replace table water_quality (
    water_id int references water(water_id),
    water_temp number,
    salinity number,
    ph number,
    nh3_n_mgl number,
    no3_mgl number,
    date datetime
);

create or replace table fish_data (
    fish_id int references fish(fish_id),
    region_id int references region(region_id),
    sample_size int,
    avg_size number,
    min_size number,
    max_size number,
    date datetime
);