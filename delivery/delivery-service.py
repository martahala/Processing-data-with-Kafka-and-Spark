from kafka import KafkaConsumer
import csv
import io

#Initialize the Kafka consumer to consume messages from the 'data-topic'
consumer = KafkaConsumer(
    'data-topic',  #Kafka topic to consume from
    bootstrap_servers='kafka:9092',  #Kafka broker address
    group_id=None,  #Kafka consumer group ID (it will consume all messages)
    auto_offset_reset='earliest'  #Start reading from the earliest message
)

def process_csv_data(record):
    """
    The function processes the CSV data from a Kafka record.

    Parameters:
    record (str): The raw CSV data in string format to be processed.

    Returns:
    None
    """
    try:
        #Ensure the record is not empty
        if not record.strip():
            print("Empty record received")
            return

        #Use StringIO to simulate a file-like object for CSV reading
        f = io.StringIO(record)
        reader = csv.reader(f)
        
        #Read the first row (header) and the second row (data)
        row = next(reader)  #CSV data will be in the first row
        print(f"Processed record: {row}")

    except Exception as e:
        #Log any error encountered while processing the CSV record
        print(f"Error processing CSV: {e}")

#Consume messages from Kafka
for message in consumer:
    """
    Consume messages from the Kafka topic and process the CSV data.
    The 'message.value.decode('utf-8')' decodes the raw byte data into a string format suitable for processing as CSV.
    """
    record = message.value.decode('utf-8')  #Decode the byte message to string

    #Log the raw message for debugging
    print(f"Received message: {record}")
    
    #Process the CSV data from the record
    process_csv_data(record)

