from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col, count, avg
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

#Initialize Spark session
spark = SparkSession.builder.appName("StreamingAggregationExample").getOrCreate()

#Define schema for the incoming data
schema = StructType([
    StructField("key", StringType(), True),
    StructField("value", StringType(), True),
    StructField("timestamp", StringType(), True)
])

#Create a streaming DataFrame from Kafka source (example)
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "data-topic") \
    .load()

#Convert 'key' and 'value' columns to string type
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp")

#Convert timestamp to proper type
df = df.withColumn("timestamp", col("timestamp").cast("timestamp"))

#Add watermark to the streaming Data Frame
df_with_watermark = df.withWatermark("timestamp", "1 minute")

#Perform sliding window aggregation 
#The window size is 5 minutes. The slide duration is 1 minute.
aggregated_df = df_with_watermark \
    .groupBy(window(col("timestamp"), "5 minutes", "1 minute"), "key") \
    .agg(
        count("value").alias("message_count"), #Count the number of messages per window per key
        avg(col("value").cast("double")).alias("avg_value") #Calculate the average value of 'value'
    )

#Write the output stream to console 
query = aggregated_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

#Await termination of the stream
query.awaitTermination()
