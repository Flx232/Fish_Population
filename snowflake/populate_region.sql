use role sysadmin;
use warehouse COMPUTE_WH;
use database FLORIDA_DB;
use schema water_quality_fisheries;

create or replace STAGE region_stage
    directory = (enable = true)
    encryption = (type = 'SNOWFLAKE_SSE');

put 'file:///opt/airflow/in/parquet/region/*.parquet' @region_stage;

create or replace file format REGION_PARQUET
    type = 'PARQUET'
    compression = 'SNAPPY'
    binary_as_text = true
    use_logical_type = true;

create or replace table raw_region_parquet (
    reg variant
);

copy into raw_region_parquet
from (
    select
        $1
    from @region_stage
    (file_format => REGION_PARQUET)
);

insert into region (name)
select distinct
        trim(reg:RegionName::string) as region
    from raw_region_parquet;


insert into water (name, region_id)
select distinct
        trim(reg:WaterBodyName::string) as water, region_id
    from raw_region_parquet r join region g on g.name = trim(r.reg:RegionName::string);