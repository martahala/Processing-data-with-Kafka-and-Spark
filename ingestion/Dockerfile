# Use a Python base image
FROM python:3.9-slim

# Install Kafka-Python
RUN pip install pyspark kafka-python


# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Set the entrypoint for the container
CMD ["python", "ingestion-service.py"]



