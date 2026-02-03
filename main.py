import finnhub
import os
from dotenv import load_dotenv
import websocket

load_dotenv()

API_KEY = os.getenv("FIZZHUB_API_KEY")

finnhub_client = finnhub.Client(api_key=API_KEY)

# print(finnhub_client.market_status(exchange='US'))

# print(finnhub_client.company_profile2(symbol='AAPL'))

print(finnhub_client.company_news('AAPL', _from="2025-12-01", to="2026-01-31"))


def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    # ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    # ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=d60p4mpr01qto1rdu59gd60p4mpr01qto1rdu5a0",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()



