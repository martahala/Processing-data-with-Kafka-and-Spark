import pandas as pd
from kafka import KafkaProducer
import time
from kafka.errors import NoBrokersAvailable

#Kafka brokers list (adjusted to the broker names and ports from your configuration)
BROKER_LIST = ['kafka:9092']  #Adjust as necessary (e.g., 'kafka:9092' for Docker)

# Initialize Kafka Producer with retry mechanism
def create_kafka_producer():
    """
    The funtion creates and returns a Kafka producer with a retry mechanism in case Kafka is unavailable.

    Returns:
         KafkaProducer: A KafkaProducer instance connected to the Kafka brokers.
    """
    producer = None #Initialize the producer as None
    while producer is None: #Retry until the producer is created successfully
        try:
            producer = KafkaProducer(
                bootstrap_servers=BROKER_LIST,  #Brokers for failover
                value_serializer=lambda v: v,  #Data is sent as raw bytes (no serialization needed)
                request_timeout_ms=120000  #Timeout for requests
            )
            print("Connected to Kafka broker.")
        except NoBrokersAvailable:
            print("Waiting for Kafka to be available...")
            time.sleep(5)  #Retry every 5 seconds until Kafka is ready
        except Exception as e:
            print(f"Error creating producer: {e}")
            time.sleep(5)  #Retry on other errors as well
    return producer #Return the successfully created producer

# Load your dataset (CSV in this case)
dataset_path = '/Users/marththe/Desktop/docker/ingestion/data.csv'  # Path inside the Docker container

def produce_data():
    """
    The function loads a dataset and sends it as raw CSV strings to a Kafka topic.
    
    Returns:
          None
    """
    #Load the dataset using pandas
    try:
        df = pd.read_csv(dataset_path)
        print(f"Loaded dataset with {len(df)} records.") #Log the number of records loaded
    except Exception as e:
        print(f"Error loading dataset: {e}") #Handle errors that might occur while loading the dataset
        return

    #Initialize Kafka Producer
    producer = create_kafka_producer()

    #Check if producer is None
    if producer is None:
        print("Producer was not created, cannot send data.")
        return
    
    #Limit the number of records to test (e.g., 10 records)
    for index, row in df.head(10).iterrows():  #Only use first 10 rows for testing
        # Convert each row into a CSV string 
        row_str = ','.join(str(val) for val in row)  #Convert row values into a comma-separated string
        try:
            producer.send('data-topic', row_str.encode('utf-8'))  #Send as a raw CSV string (encoded as UTF-8 bytes) to the Kafka topic 'data-topic'
            print(f"Produced: {row_str}") #Log the sent record
        except Exception as e:
            print(f"Error sending data: {e}") #Handle any errors encountered while sending data to Kafka
        
        #Simulate real-time ingestion (send one record per second)
        time.sleep(1)

if __name__ == '__main__':
    """
    Main entry point for the script. Calls 'produce_data()' to initiate data production and sending.

    Returns:
         None
    """
    try:
        produce_data() #Start the data production and sending process
    except KeyboardInterrupt:
        print("Data production interrupted by user.") #Handle user interruption gracefully
