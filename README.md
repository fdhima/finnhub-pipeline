# finnhub-pipeline

Architecture:
```
Finnhub WebSocket
   ↓
Python WebSocket client
   ↓
Kafka Producer
   ↓
Kafka Topic
   ↓
Kafka Consumer
   ↓
Stream Processor with Flink (for law-latency streaming)
   ↓
Data Lake / Lakehouse (Parquet + Delta/Iceberg)
   ↓
Data Warehouse (Modeled tables)
   ↓
BI Tool

```


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


# Apache Flink

Using Stream Processor for continuously analyzing and processing data as it is generated with the purpose of enabling real-time insights into those streamed data.

This component consumes Kafka topics and performs transformations/analytics in real time.


Choosed Apache Flink for it low latency. Another appoach would be Apache Spark, since it offers easy Python intergration.

```
Kafka Topic: finnhub.trades
        │
        ▼
Apache Flink Job
   - Windowing: 1 min / 5 min VWAP
   - Filtering: Symbol-based
   - Aggregation: Volume, Price stats
        │
        ▼
Output Kafka Topic: finnhub.analytics
        │
        ▼
Consumer / Dashboard / Storage
```

Install Apache Flink via Docker:
```bash
docker pull flink:scala_2.12-java21
```

