from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

spark = SparkSession.builder.appName("FloridaApp").getOrCreate()
revenue_df = spark.read.csv(
    "/opt/spark/files/in/Tampa_Bay_Revenue.csv", header=True, inferSchema=True
)
revenue_df = revenue_df.withColumn('RegionName', lit('Tampa Bay Region'))
revenue_df.write.parquet("/opt/spark/files/out/parquet/revenue", mode="overwrite")
spark.stop()