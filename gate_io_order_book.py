import json
import logging
import time
from websocket import create_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_order_book():
    url = "wss://api.gateio.ws/ws/v4/"

    ws = create_connection(url)
    logger.info('WebSocket connected')

    # Subscribe to the order book channel for a specific trading pair
    symbol = "btc_usdt"
    ws.send(json.dumps({
        "channel": f"spot.order_book.{symbol}",
        "event": "subscribe",
        "payload": {
            "asks": 100,
            "bids": 100
        }
    }))

    # Wait for the initial order book snapshot
    while True:
        result = ws.recv()
        data = json.loads(result)
        if data.get("event") == "subscribed" and data.get("channel") == f"spot.order_book.{symbol}":
            break

    # Process the received order book snapshot
    if "asks" in data["payload"] and "bids" in data["payload"]:
        print("Order Book Data:")
        print("Asks:")
        for ask in data["payload"]["asks"]:
            print(ask)
        print("Bids:")
        for bid in data["payload"]["bids"]:
            print(bid)

    # Close the WebSocket connection
    ws.close()
    logger.info('WebSocket connection closed')


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)
    get_order_book()

