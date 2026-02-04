import json
import time
import random
from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def get_dummy_data():
    return {
        'sensor_id': random.randint(1, 100),
        'temperature': round(random.uniform(20.0, 30.0), 2),
        'humidity': round(random.uniform(30.0, 70.0), 2),
        'timestamp': int(time.time())
    }


def main():
    msg_count = 0
    while True:
        try:
            # Connect to Kafka running on localhost:29092
            producer = KafkaProducer(
                bootstrap_servers=['localhost:29092'],
                value_serializer=json_serializer
            )
            print("Connected to Kafka!")
            break
        except Exception as e:
            print(f"Waiting for Kafka to be ready... {e}")
            time.sleep(5)

    topic_name = 'input-topic'

    print(f"Starting producer. Sending data to '{topic_name}'...")
    try:
        while True:
            data = get_dummy_data()
            producer.send(topic_name, data)
            print(f"Sent: {data}")
            time.sleep(1) # Send one message per second
    except KeyboardInterrupt:
        print("\nStopping producer...")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
