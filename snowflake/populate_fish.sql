use role sysadmin;
use warehouse COMPUTE_WH;
use database FLORIDA_DB;
use schema water_quality_fisheries;

create or replace STAGE fish_stage
    directory = (enable = true)
    encryption = (type = 'SNOWFLAKE_SSE');

put 'file:///opt/airflow/in/parquet/fish/*.parquet' @fish_stage;

create or replace file format FISH_PARQUET
    type = 'PARQUET'
    compression = 'SNAPPY'
    binary_as_text = true
    use_logical_type = true;

create or replace table raw_fish_parquet (
    f variant
);

copy into raw_fish_parquet
from (
    select
        $1
    from @fish_stage
    (file_format => FISH_PARQUET)
);

insert into fish (scientific_name, common_name)
select
    scientific,
    common
from (
    select distinct
        trim(f:Scientificname::string) as scientific,
        trim(f:Commonname::string) as common
    from raw_fish_parquet
    where f:Scientificname::string is not null
      and f:Commonname::string is not null
);