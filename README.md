README

The project provides a data ingestion, processing, and delivery pipeline built with Apache Kafka and Apache Spark, leveraging Docker for containerization and horizontal scaling. It uses partitioning for scalable Kafka topics. The pipeline is designed to handle large volumes of streaming data and perform real-time preprocessing, aggregation, and delivery to downstream systems.  

Features:
  Kafka:
    Data ingestion and streaming with Kafka.
    Horizontal scaling of Kafka brokers and topic partitioning for fault tolerance. 
  Spark:
    Real-time data processing using Spark Streaming.
    Supports various modes: client, master, and worker.
    Horizontal scaling of Spark workers for distributed processing.
  Docker:
    Docker Compose for managing multi-container services, including Kafka, Spark, and custom ingestion/processing services.
  Horizontal scaling:
    Kafka brokers and Spark workers are horizontally scaled for better performance.
    Partitioning of Kafka topics for efficient parallel data processing.
  Data pipeline components:
    Ingestion service ingests data from CSV files and streams them to Kafka.
    Preprocessing service preprocesses data via Spark before passing it to the next stage.
    Aggregation service aggregates processed data.
    Delivery service sends processed data to external systems or endpoints. 


Setup and installation
  1. Clone the repository.
  2. Build the Docker containers.
  3. Start the services (Zookeeper, Kafka brokers, Spark master and worker nodes, ingestion, preprocessing, aggregation, and delivery services).
  4. Verify the pipeline. 
    

The data are taken from https://www.kaggle.com/datasets/patrickfleith/controlled-anomalies-time-series-dataset. 
