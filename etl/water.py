from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import broadcast, col, explode, split, trim, regexp_replace, lit

spark = SparkSession.builder.appName("FloridaApp").getOrCreate()

water_region_1_df = spark.read.csv(
    "/opt/spark/files/in/clean_water_quality.csv", header=True, inferSchema=True
)

water_region_2_df = spark.read.csv(
    "/opt/spark/files/in/sgsegest.csv", header=True, inferSchema=True
)

water_region_1_df = water_region_1_df.filter(water_region_1_df['WaterBodyName'].rlike(r'\bBay\b'))
water_region_bay_1_df = water_region_1_df.select('WaterBodyName').distinct()
water_region_2_df = water_region_2_df.filter(water_region_2_df['segment'].rlike(r'\bBay\b'))
water_region_bay_2_df = water_region_2_df.select('segment').distinct()
water_region_df = water_region_bay_1_df.union(water_region_bay_2_df).distinct()
water_region_df = water_region_df.withColumn('RegionName', lit('Tampa Bay Region'))
water_region_df.write.parquet("/opt/spark/files/out/parquet/region", mode="overwrite")

water_region_2_df = water_region_2_df.withColumnRenamed('segment', 'WaterBodyName')
water_region_2_df.write.parquet("/opt/spark/files/out/parquet/seagrass", mode="overwrite")

water_region_1_df.select('SampleDate').show()
water_region_1_df = water_region_1_df.select('WaterBodyName', 'SampleDate', 'Salinity_ppt', 'TempW_F', 'pH', 'NH3_N_mgl', 'NO3_mgl')
water_region_1_df.write.parquet("/opt/spark/files/out/parquet/water_quality", mode="overwrite")
spark.stop()