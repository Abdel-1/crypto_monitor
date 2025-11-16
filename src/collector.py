import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read config variables
CSV_FILE = os.getenv("CSV_FILE_NAME")
SYMBOL = os.getenv("CRYPTO_SYMBOL").lower()

# Ensure parent directory exists (e.g., data/)
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)


async def collect():
    url = f"wss://stream.binance.com:9443/ws/{SYMBOL}@trade"

    print(f"📡 Connecting to Binance WebSocket for {SYMBOL.upper()} ...")

    async with websockets.connect(url) as ws:
        print(f"✅ Connected! Streaming real-time trades for: {SYMBOL.upper()}")

        while True:
            data = await ws.recv()
            trade = json.loads(data)

            # Extract price and timestamp
            price = float(trade["p"])
            timestamp = datetime.utcfromtimestamp(trade["T"] / 1000)


            # Create a DataFrame row
            df = pd.DataFrame([[timestamp, price]], columns=["timestamp", "price"])

            # Save to CSV (append mode)
            df.to_csv(
                CSV_FILE,
                mode="a",
                header=not os.path.exists(CSV_FILE),
                index=False,
            )

            # Print output for monitoring
            print(timestamp, price)


if __name__ == "__main__":
    asyncio.run(collect())
