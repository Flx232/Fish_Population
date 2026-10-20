import json
import pendulum

from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.http.operators.http import HttpOperator
from airflow.sdk import dag

@dag(
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["board game geeks", "sql_spark"],
)
def bgg_dag():
    bgg_schema = SQLExecuteQueryOperator(
        task_id="bbg_schema",
        sql="/bgg_sql/bgg.sql",
        conn_id="pg_conn",
    )

    data = {"app": "bgg_app.py"}
    bgg_http_task = HttpOperator(
        task_id="bgg_http_task",
        http_conn_id="http_spark",
        method="POST",
        headers={"Content-Type": "application/json"},
        endpoint="/submit",
        data=json.dumps(data),
    )

    bgg_schema >> bgg_http_task

bgg_dag()