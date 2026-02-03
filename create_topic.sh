docker exec -it <container_name> \
  /opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic finnhub.trades \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
