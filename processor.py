from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer

def main():
    # Create the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    # Add the Flink Kafka Connector JAR
    # Ensure you look for the jar in the current directory or provide the full path
    import os
    jar_path = f"file://{os.getcwd()}/flink-sql-connector-kafka-4.0.0-2.0.jar"
    print(f"Loading JAR from: {jar_path}")
    env.add_jars(jar_path)
    
    # Define the Kafka Source
    source = KafkaSource.builder() \
        .set_bootstrap_servers("localhost:29092") \
        .set_topics("input-topic") \
        .set_group_id("flink-processor-group") \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    # Create the DataStream
    ds = env.from_source(source, watermark_strategy=WatermarkStrategy.no_watermarks(), source_name="Kafka Source")

    # Simple processing: Just print the data to stdout (which goes to TaskManager logs or console)
    ds.print()

    # Execute the job
    env.execute("Flink Kafka Dummy Processor")

if __name__ == "__main__":
    main()
