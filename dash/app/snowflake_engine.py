import os
import snowflake.connector

def _connect():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role=os.environ.get("SNOWFLAKE_ROLE"),
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ.get("SNOWFLAKE_DATABASE"),
        schema=os.environ.get("SNOWFLAKE_SCHEMA"),
        client_session_keep_alive=False,
    )

def query(sql: str, params: tuple | None = None) -> list[dict]:
    with _connect() as conn:
        with conn.cursor(snowflake.connector.DictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetch_pandas_all()