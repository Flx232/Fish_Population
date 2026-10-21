use role sysadmin;
use warehouse COMPUTE_WH;
use database FLORIDA_DB;
use schema water_quality_fisheries;

insert into fish_data (fish_id, region_id, sample_size, avg_size, min_size, max_size, date)
select
    fish_id, 
    region_id, 
    trim(f:TotalNum::int) as sample_size, 
    trim(f:avg_size::number) as avg_size,
    trim(f:min_size::number) as min_size,
    trim(f:max_size::number) as max_size,
    to_timestamp_tz(trim(f:Sampling_Date::string), 'YYYY/MM/DD HH24:MI:SSTZH')::timestamp_ntz as sampling_date
    from raw_fish_parquet r
    join fish f on f.scientific_name = trim(r.f:Scientificname::string) and f.common_name = trim(r.f:Commonname::string)
    join region g on g.name = trim(r.f:RegionName::string);