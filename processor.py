import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.datastream.connectors.jdbc import JdbcSink
from pyflink.datastream.connectors.jdbc import JdbcConnectionOptions, JdbcExecutionOptions
from pyflink.common.typeinfo import RowTypeInfo, Types


def main():
    # Create the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    env.enable_checkpointing(10000)

    env.add_jars(
        f"file://{os.getcwd()}/flink-sql-connector-kafka-4.0.0-2.0.jar",
        f"file://{os.getcwd()}/flink-connector-jdbc-3.1.2-1.17.jar",
        f"file://{os.getcwd()}/postgresql-42.7.3.jar",
    )

    def jdbc_statement_builder(ps, x):
        ps.setString(1, x)

    sink = JdbcSink.sink(
        "INSERT INTO events (value) VALUES (?)",
        # type_info=RowTypeInfo([Types.STRING()]),
        RowTypeInfo([Types.STRING()]),
        jdbc_statement_builder,
        # JdbcExecutionOptions.builder()
        #     .with_batch_size(1000)
        #     .build(),
        JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
            .with_url("jdbc:postgresql://localhost:5432/postgres")
            .with_driver_name("org.postgresql.Driver")
            .with_user_name("postgres")
            .with_password("password")
            .build()
    )

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

    ds.add_sink(sink)

    # Execute the job
    env.execute("Flink Kafka Dummy Processor")

if __name__ == "__main__":
    main()
