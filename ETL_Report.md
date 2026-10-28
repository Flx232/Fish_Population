# ETL Report
## Data Source
1.  Tampa Port Authority (2025) Annual Revenue Report https://flauditor.gov/pages/specialdistricts_efile%20rpts/2025%20tampa%20port%20authority.pdf
    1.  "Date of access: 10/12/2026
2.  Tampa Bay Estuary Program (2026-07-13) sgsegest https://tbep-tech.r-universe.dev/datasets
    1.  "Date of access: 10/5/2026
3.  Sarasota County wateratlas Water Quality 2026 https://sarasota.wateratlas.usf.edu/DataDownload/Default.aspx
    1.  Date of access: 10/10/2026
4.  Florida Fish and Wildlife Conservation Commission 2025 FL_Fisheries_Independent_Monitoring_Inshore_Stratified-Random_Sampling_Records,  https://data.florida-seacar.org/programs/details/69
    1.  Date of access: 10/11/2026

## Extraction
1. Data for Sarasota County wateratlas Water Quality was sourced from the Sarasota County wateratlas website. The data was downloaded after selecting data from a user interface. The format of the data downloaded as an xls file, which requires converting into a csv file first and then further processing as an excel file.
   1. First load the dirty csv file ont a power query worksheet
   2. Remove unnecessary columns that contain majority null values
   3. The data contains 
   4. Filter out some of the measurements in the aggregate column
   5. Pivot an aggregated measurement column into multiple measurement columns
2. Tampa Port Authority Annual Revenue Report. The data was manually recorded on a custom csv file based on a pdf report of the tampa bay revenue generation.
3. Stratified Random Sampling Fisheries data was sourced from the Florida Fish and Wildlife Conservation Commission linked by ChatGPT. The data itself contains a csv file as well as many other different file types to download. No further processing of data was required
4. Sgsegest data was sourced from the Tampa Bay Estuary Program github repository. The repository contains a search bar to look for different data stored in the repository, including sea grass segment estimation data. Multiple different file type choices were provided, including csv.

### water ETL
1. Water body data contains other water body other than bay. Had to specify I was only looking at bay data rather than bayous, canals, tributaries and rivers.
2. Joined the water quality data and seagrass data for future ease of populating snowflake table

## fish ETL
1. Filter out fish data recorded by a tampa bay monitor as the data contains fish sampling from multiple different fisheries around Florida.

## revenue ETL
1. The data was loaded as a csv file as is to be further processed in snowflake

## Snowflake loading
1. Independent tables, such as fish table and region table were populated first.
2. Other tables were populated directly from the csv file
3. Revenue csv was split into 4 different tables and 1 type table
   1. This is to ensure the data is organized rather than blindly populating 1 table and having it be a wide table.

## ETL Lifecycle
Shown in /dash/app/assets/airflow.png