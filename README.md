README

The project aims to build a real-time data backend for a data-intensive application.

The project sets up a Kafka-based data streaming platform with Spark for processing.  The services include Kafka brokers, Spark master and ingestion, preprocessing, aggregation, and delivery services. 
Key components: 
	Zookeeper is used to manage Kafka broker data.
	Kafka is used to handle the data pipeline. 
	Spark
	    Spark Master coordinates the Spark cluster.
	    Spark Workers execute the Spark jobs.
	Ingestion service ingests data into Kafka.
	Preprocessing service processes data from Kafka streams using Spark.
	Aggregation service aggregates the processed data.
	Delivery service delivers the processed results. 
Features: 
•	Horizontal Scaling
•	Partitioning
•	Checkpointing
•	Replication mechanism


The data is taken from https://www.kaggle.com/datasets/patrickfleith/controlled-anomalies-time-series-dataset. 
