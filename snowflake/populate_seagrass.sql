use role sysadmin;
use warehouse COMPUTE_WH;
use database FLORIDA_DB;
use schema water_quality_fisheries;

create or replace STAGE grass_stage
    directory = (enable = true)
    encryption = (type = 'SNOWFLAKE_SSE');

put 'file:///opt/airflow/in/parquet/seagrass/*.parquet' @grass_stage;

create or replace file format GRASS_PARQUET
    type = 'PARQUET'
    compression = 'SNAPPY'
    binary_as_text = true
    use_logical_type = true;

create or replace table raw_grass_parquet (
    g variant
);

copy into raw_grass_parquet
from (
    select
        $1
    from @grass_stage
    (file_format => GRASS_PARQUET)
);

insert into seagrass (water_id, acres, year)
select
    water_id, 
    trim(g:acres::number) as acres, 
    trim(g:year::int) as year
    from raw_grass_parquet r
    join water w on w.name = trim(r.g:WaterBodyName::string);