import json
import pendulum

from airflow.sdk import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.http.operators.http import HttpOperator

@dag(
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["snowflake", "spark"],
    template_searchpath="/opt/airflow"
)
def snowflake_dag():
    snowflake_schema = SQLExecuteQueryOperator(
        task_id="snowflake_schema",
        sql="/sql/florida.sql",
        conn_id="snowflake_conn",
    )

    data = {"app": "fish.py"}
    fish_http_task = HttpOperator(
        task_id="fish_http_task",
        http_conn_id="http_spark",
        method="POST",
        headers={"Content-Type": "application/json"},
        endpoint="/submit",
        data=json.dumps(data),
    )

    data = {"app": "revenue.py"}
    revenue_http_task = HttpOperator(
        task_id="revenue_http_task",
        http_conn_id="http_spark",
        method="POST",
        headers={"Content-Type": "application/json"},
        endpoint="/submit",
        data=json.dumps(data),
    )

    data = {"app": "water.py"}
    water_http_task = HttpOperator(
        task_id="water_http_task",
        http_conn_id="http_spark",
        method="POST",
        headers={"Content-Type": "application/json"},
        endpoint="/submit",
        data=json.dumps(data),
    )

    populate_region = SQLExecuteQueryOperator(
        task_id="populate_region",
        sql="/sql/populate_region.sql",
        conn_id="snowflake_conn",
    )

    populate_fish = SQLExecuteQueryOperator(
        task_id="populate_fish",
        sql="/sql/populate_fish.sql",
        conn_id="snowflake_conn",
    )

    populate_seagrass = SQLExecuteQueryOperator(
        task_id="populate_seagrass",
        sql="/sql/populate_seagrass.sql",
        conn_id="snowflake_conn",
    )

    populate_fish_data = SQLExecuteQueryOperator(
        task_id="populate_fish_data",
        sql="/sql/populate_fish_data.sql",
        conn_id="snowflake_conn",
    )

    populate_revenue = SQLExecuteQueryOperator(
        task_id="populate_revenue",
        sql="/sql/populate_revenue.sql",
        conn_id="snowflake_conn",
    )

    populate_water_data = SQLExecuteQueryOperator(
        task_id="populate_water_data",
        sql="/sql/populate_water_data.sql",
        conn_id="snowflake_conn",
    )

    snowflake_schema >> [fish_http_task, revenue_http_task, water_http_task]
    fish_http_task >> populate_fish
    water_http_task >> populate_region
    revenue_http_task >> populate_revenue
    # populate_region >> populate_water_data
    populate_region >> [populate_revenue, populate_seagrass, populate_fish_data, populate_water_data]
    populate_fish >> populate_fish_data

snowflake_dag()