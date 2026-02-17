#!/bin/bash
set -e

# Download Flink Kafka Connector
# Using version 4.0.0-2.0 compatible with Flink 2.x
JAR_VERSION="4.0.0-2.0"
JAR_NAME="flink-sql-connector-kafka-${JAR_VERSION}.jar"
JAR_URL="https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/${JAR_VERSION}/${JAR_NAME}"
JDBC_JAR = f"https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc-core/${JAR_VERSION}/"

# Update code to download all the needed JARs

if [ ! -f "$JAR_NAME" ]; then
    echo "Downloading $JAR_NAME..."
    wget "$JAR_URL"
else
    echo "$JAR_NAME already exists."
fi

# Create and activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Virtual environment already exists."
    # Ensure dependencies are up to date
    source venv/bin/activate
    pip install -r requirements.txt
fi

echo "Setup complete. To activate the venv, run: source venv/bin/activate"
