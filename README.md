# Capstone
## Interest:
- Water Temperature of Tampa Bay Florida
- Marine life population of Tampa Bay Florida
- Human made chemicals, specifically pesticides and herbicides, in Tampa Bay Florida estuary
- PH Level in the water.
- chemical amount in water sampling in Tampa Bay Florida
- Sea Grass survey in Tampa Bay Florida.
- Construction around Tampa Bay over the years.
- Large vessel presence in Tampa Bay
## Hypotheses
- There is a direct correlation between human anthropomorphic climate change and a decline in marine life population in Tampa Bay.
- Chemical dumps of pesticides do not have as large of an impact as climate change
- Higher PH is caused by increasing temperature of water
- PH change and types of dissolved gasses in the water 
- A growth in Sea Grass has a positive correlation with the population of marine life in the area.
- Increase of vessel presence leads to the decline of marine life and sea grass growth.
## Tasks
- Exploratory Data Analysis of each dataset
- Importing data (from CSV, database, API, etc.)
- Data cleaning: include where (Airflow, Jupyter) and how (Pandas, Spark, Dask, Polars)
- Database design (ERD, DDL)
- Other data storage: databases, blobs, etc.
- ETL (process and documentation)
- Airflow DAGs
- ML model (optional): training, tuning
- Sketches: visualizations and dashboards
- Dashboard creation
- Presentation prep: creation, practice, contingencies
## Plan
### Data Collection
- Collect relevant data to be used in the project. This consists of water quality over the years, marine population over the years, sea grass growth and presence of vessels in the region.
### Evaluating Data
- First understand the make up of each dataset. Some are xlsx, some are csv.
    - Clean xlsx files in excel to speed up the process using power queries.
    - Convert xlsx files into csv files.
- Design a pipeline using spark and airflow that will clean the data
- Understand the usage of specific key words and determine how they will connect to each other in the database and later in visualization
- Think of ways how we can reshape the table to only contain useful information
- Plot visualizations that would further help us understand what is needed for visualization
- Explore some Machine learning models I can potentially use to experiment with predicting values in the future and show future trends in the region.
- Estimated Time: 14 Hours
### Creating Schema and Database
- Look at the columns in the datasets we plan to use
- Bunch columns based on similarities
- Create small tables containing these specific columns
- Slowly create relations between these tables
  - Add many to many tables if needed
- Confirm final output with a third party
- Create database in postgres server
- Estimated Time 5 Hours
### ETL Pipeline
- Refer to previous projects for creating ETL pipeline
- Conduct exploratory transformations in the notebook
- Implement these transformations 
- Create pytest for every transformation and the ETL pipeline
- Tie in the populating of database and the ETL pipeline together using spark and airflow
- Estimated Time 24 Hours
### SQL Queries extraction
- Do mock sql retrieval queries
- This is to prepare for extracting data for generating visualizations 
- Estimated Time 2-3 Hours
### ML
- Select specific columns that will work well in specific machine learning models
    - Quantitative data for linear regression
- Explore with snowflake to transfer data into the cloud and experiment with the notebook.
- Alternatively can use pandas to do some ML exploration. Use these models later in generating visualizations.
- Estimated Time 12 Hours
### Sketching Visualizations
- Refer to previous projects for designing sketch
- Provide sketch as review to other people and receive feedback
- Re-iterate the feedback into the plan
- Consider making multi-page dashboard
- Estimated Time 4-6 Hours
### Generating Visualizations
- Refer to previous projects for creating visualizations
- Refer to previous callback (Hover data, etc for more interesting data visualizations)
- Refer to exploratory notebook
- Utilize tested SQL queries
- Estimated Time 36 Hours
### Presentation Preparations
- Utilize previous README reports for each step of the plan to create a baseline idea as to how the presentation will be displayed
- Explain the reason for creating the dashboard and passion behind it
- Point out the hypothesis made at the beginning of the project
- Describe what are some parts of the process I find the most difficult and how I overcame these difficulties.
- Select key and interesting data visualization to highlight my hypothesis
- phase towards showing dashboard
#### Practice Plan
- Create a script to refer to, not to directly follow along
- Try practicing presenting 10 times a day 2-3 days before the deadline.
- Perhaps consider recording each attempt to ascertain how the presentation would sound to an audience
## Setting up Environment
- python -m venv .
- pip install -r requirements.txt

Total Hours Required: 97-100 hours at least