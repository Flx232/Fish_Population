use role sysadmin;
use warehouse COMPUTE_WH;
use database FLORIDA_DB;
use schema water_quality_fisheries;

create or replace STAGE water_stage
    directory = (enable = true)
    encryption = (type = 'SNOWFLAKE_SSE');

put 'file:///opt/airflow/in/parquet/water_quality/*.parquet' @water_stage;

create or replace file format WATER_PARQUET
    type = 'PARQUET'
    compression = 'SNAPPY'
    binary_as_text = true
    use_logical_type = true;

create or replace table raw_water_parquet (
    wa variant
);

copy into raw_water_parquet
from (
    select
        $1
    from @water_stage
    (file_format => WATER_PARQUET)
);

insert into water_quality (water_id, water_temp, salinity, ph, nh3_n_mgl, no3_mgl, date)
select
    water_id, 
    trim(wa:TempW_F::number) as water_temp, 
    trim(wa:Salinity_ppt::number) as salinity, 
    trim(wa:pH::number) as ph,
    trim(wa:NH3_N_mgl::number) as nh3_n_mgl,
    trim(wa:NO3_mgl::number) as no3_mgl,
    to_timestamp_ntz(trim(wa:SampleDate::string), 'MM/DD/YYYY HH24:MI')::date as sampling_date
    from raw_water_parquet r
    join water w on w.name = trim(r.wa:WaterBodyName::string);