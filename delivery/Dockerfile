# Use the official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies (Kafka and any other required packages)
RUN pip install kafka-python pandas

# Copy the delivery-service.py script into the container
COPY delivery-service.py /app/delivery-service.py

# Set the command to run the service
CMD ["python", "delivery-service.py"]

