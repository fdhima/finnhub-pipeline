from confluent_kafka import Consumer

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "debug-consumer",
    "auto.offset.reset": "latest"
})

consumer.subscribe(["finnhub.trades"])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(msg.error())
    else:
        print(msg.value().decode("utf-8"))
