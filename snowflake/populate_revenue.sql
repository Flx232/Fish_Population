use role sysadmin;
use warehouse COMPUTE_WH;
use database FLORIDA_DB;
use schema water_quality_fisheries;

create or replace STAGE revenue_stage
    directory = (enable = true)
    encryption = (type = 'SNOWFLAKE_SSE');

put 'file:///opt/airflow/in/parquet/revenue/*.parquet' @revenue_stage;

create or replace file format REVENUE_PARQUET
    type = 'PARQUET'
    compression = 'SNAPPY'
    binary_as_text = true
    use_logical_type = true;

create or replace table raw_revenue_parquet (
    rev variant
);

copy into raw_revenue_parquet
from (
    select
        $1
    from @revenue_stage
    (file_format => REVENUE_PARQUET)
);

insert into dock_type (type) values ('Dockage'), ('Wharfage');

insert into dock_revenue (region_id, cargo, cruise, other, dock_type_id, year)
select
    region_id,
    cargo,
    cruise,
    other,
    dock_type_id,
    year
    from (
        select 'Dockage' as type, 
            rev:Year::number as year,
            rev:RegionName::string as region,
            rev:dockage_Cargo::number as cargo,
            rev:dockage_Cruise::number as cruise,
            rev:dockage_Other::number as other
        from raw_revenue_parquet
        union all
        select 'Wharfage' as type, 
            rev:Year::number as year,
            rev:RegionName::string as region,
            rev:wharfage_Cargo::number as cargo,
            rev:wharfage_Cruise::number as cruise,
            rev:wharfage_Other::number as other
        from raw_revenue_parquet
    ) u 
    join region r on u.region = r.name
    join dock_type d on u.type = d.type;

insert into region_revenue (region_id, net_investment, port_usage_fee, land_lease, year)
select
    region_id,
    rev:Net_Investment::number,
    rev:Port_Usage_fees::number,
    rev:Land_lease::number,
    rev:Year::number
    from raw_revenue_parquet r
    join region g on trim(r.rev:RegionName::string) = g.name;

insert into cargo (region_id, dry, liquid, general, year)
select
    region_id,
    trim(rev:Dry_Cargo::number),
    trim(rev:Liquid_Cargo::number),
    trim(rev:General_Cargo::number),
    trim(rev:Year::number)
    from raw_revenue_parquet r
    join region g on trim(r.rev:RegionName::string) = g.name;

insert into cruise (region_id, passenger_count, revenue, year)
select
    region_id,
    rev:Cruise_Passenger_Count::number,
    rev:Cruise_Revenue::number,
    rev:Year::number
    from raw_revenue_parquet r
    join region g on trim(r.rev:RegionName::string) = g.name;