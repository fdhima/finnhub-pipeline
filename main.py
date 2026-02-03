import time
import finnhub
import os
from dotenv import load_dotenv
import websocket
from confluent_kafka import Producer
import json


load_dotenv()


API_KEY = os.getenv("FIZZHUB_API_KEY")
KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:9092",
    "linger.ms": 5,
    "acks": "all"
}

finnhub_client = finnhub.Client(api_key=API_KEY)
producer = Producer(KAFKA_CONFIG)

# print(finnhub_client.market_status(exchange='US'))

# print(finnhub_client.company_profile2(symbol='AAPL'))

# print(finnhub_client.company_news('AAPL', _from="2025-12-01", to="2026-01-31"))

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")


def on_message(ws, message):
    try:
        data = json.loads(message)

        enriched = {
            "source": "finnhub",
            "received_at": time.time(),
            "payload": data
        }

        producer.produce(
            topic="finnhub.trades",
            key=data["data"][0]["s"],
            value=json.dumps(enriched).encode("utf-8"),
            callback=delivery_report
        )

        producer.poll(0) # serve delivery callbacks
    except Exception as e:
        print(f"Kafka error: {e}")
    # print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")
    producer.flush()

def on_open(ws):
    # ws.send('{"type":"subscribe","symbol":"AAPL"}')
    # ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=d60p4mpr01qto1rdu59gd60p4mpr01qto1rdu5a0",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()



