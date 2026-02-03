# finnhub-pipeline

Architecture:
```
Finnhub WebSocket
   ↓
   (Confluent CLI)
Python WebSocket client
   ↓
Kafka Producer
   ↓
Kafka Topic
   ↓
Consumers
   ↓
Stream Processor (Spark / Flink)
   ↓
Data Lake / Lakehouse (Parquet + Delta/Iceberg)
   ↓
Data Warehouse (Modeled tables)
   ↓
BI Tool

```

WebSocket

Streaming Script

# Apache Kafka

Install Apache Kafka via Docker:
```bash
docker pull apache/kafka:4.1.1
```

Start container form Apache Kafka image:
```bash
docker run --name apache-kafka -it -d -p 9092:9092 apache/kafka:4.1.1
```

Create a Kafka topic:
```bash
docker exec -it apache-kafka \
  /opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic finnhub.trades \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
```

Verify the topic:
```bash
docker exec -it apache-kafka \
  /opt/kafka/bin/kafka-topics.sh \
  --list \
  --bootstrap-server localhost:9092
```

Create ands activate virtual environment (Linux):
```bash
python -m venv venv
source venv/bin/activate
```

Start consumer:
```bash
python3 consumer.py
```

Start producer (stream data from Funnhub API):
```bash
python3 producer.py
```
