from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema

env = StreamExecutionEnvironment.get_execution_environment()

# Kafka consumer
consumer = FlinkKafkaConsumer(
    topics='finnhub.trades',
    deserialization_schema=SimpleStringSchema(),
    properties={'bootstrap.servers': 'localhost:9092', 'group.id': 'flink-group'}
)
stream = env.add_source(consumer)

# Example: simple transformation
processed = stream.map(lambda msg: msg.upper())  # just an example

# Kafka producer
producer = FlinkKafkaProducer(
    topic='finnhub.analytics',
    serialization_schema=SimpleStringSchema(),
    producer_config={'bootstrap.servers': 'localhost:9092'}
)
processed.add_sink(producer)

env.execute("Finnhub Real-Time Stream")
