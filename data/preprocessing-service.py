import os
from pyspark.sql import SparkSession

#Set the necessary Kafka dependencies in the environment
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1,org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.1 pyspark-shell'

def create_spark_session():
    """ 
    The function creates and configures a Spark session for streaming.
    
    Returns:
        SparkSession: The created Spark session object for streaming.
    """
    print("Creating Spark session...")
    spark = SparkSession.builder \
        .appName("Kafka-PySpark-Stream-Verify") \
        .config("spark.master", "spark://pyspark-master:7077") \
        .getOrCreate()
    print("Spark session created successfully.")
    return spark

def process_stream(spark, input_topic, checkpoint_path):
    """
    The fucntion processes a stream of data from Kafka topic and writes it to the console.

    Args:
         spark(SparkSession):  The Spark session object is created by the 'create_spark_session()' function.
         input_topic (str): The Kafka topic from which data is being read.
         checkpoint_path (str): The path to store the checkpoint information from stream processing to maintain state across job restarts.
    
    Raises:
        Exception: If there is an error while processing the strem, an exception is raised and logged.
    """
    try:
        #Read the incoming Kafka stream
        print(f"Reading stream from Kafka topic: {input_topic}...")
        kafka_stream_df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "kafka:9092") \
            .option("subscribe", input_topic) \
            .option("startingOffsets", "earliest") \
            .load()

        print("Stream read from Kafka successfully.")

        #For verification, just select 'key' and 'value' columns as they are
        kafka_stream_df = kafka_stream_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

        #Write the streaming data to console for verification
        query = kafka_stream_df.writeStream \
            .outputMode("append") \
            .format("console") \
            .option("checkpointLocation", checkpoint_path) \
            .foreachBatch(lambda df, epoch_id: df.show()) \
            .start()

        print("Query started, awaiting termination...")
        query.awaitTermination()  #Correct placement for awaitTermination
        print("Query terminated.")

    except Exception as e:
        print(f"Error in processing stream: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    """
    Main entry point for the Spark Streaming job.

    Raises:
         Exception: If there is an error while starting the streaming process, an exception is raised and logged.
    """
    try:
        print("Starting Spark Streaming job...")
        spark = create_spark_session()
        input_topic = "data-topic"  #Kafka topic to read from
        checkpoint_path = "./checkpoint"  #Checkpoint path to maintain state during restarts

        #Start reading from Kafka and check if it's working
        process_stream(spark, input_topic, checkpoint_path)

    except Exception as e:
        print(f"Error in main process: {e}")
        import traceback
        traceback.print_exc()


