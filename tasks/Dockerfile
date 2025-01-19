# Use the official slim Python image
FROM python:3.12.8-slim

# Set up a consistent working directory
WORKDIR /app

# Copy application files to the container
COPY . /app

# Install system dependencies required for SSL and MongoDB
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libssl-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set up environment variables for MongoDB and other secrets
ARG MONGODB_URI
ENV MONGODB_URI=${MONGODB_URI}

ARG BRAPI_TOKEN
ENV BRAPI_TOKEN=${BRAPI_TOKEN}

# Entry point for the application
ENTRYPOINT ["python"]
