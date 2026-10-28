from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

spark = SparkSession.builder.appName("FloridaApp").getOrCreate()
fish_df = spark.read.csv(
    "/opt/spark/files/in/FL_Fisheries_Independent_Monitoring_Inshore_Stratified-Random_Sampling_Records.csv", header=True, inferSchema=True
)
tampa_fish_df = fish_df.filter(fish_df['Reference'].contains('TBM'))
tampa_fish_df = tampa_fish_df.select('Sampling_Date', 'Scientificname', 'Commonname', 'TotalNum', 'avg_size', 'min_size', 'max_size')
tampa_fish_df = tampa_fish_df.withColumn('RegionName', lit('Tampa Bay Region'))
tampa_fish_df.write.parquet("/opt/spark/files/out/parquet/fish", mode="overwrite")
spark.stop()