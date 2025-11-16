import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime

# CSV file where data will be saved
CSV_FILE = "btc_prices.csv"

async def collect():
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    async with websockets.connect(url) as ws:
        while True:
            data = await ws.recv()
            trade = json.loads(data)

            price = float(trade['p'])
            timestamp = datetime.utcfromtimestamp(trade['T'] / 1000)

            df = pd.DataFrame([[timestamp, price]], columns=["timestamp", "price"])
            df.to_csv(CSV_FILE, mode="a", header=not pd.io.common.file_exists(CSV_FILE), index=False)

            print(timestamp, price)

asyncio.run(collect())
