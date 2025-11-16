import requests
import pandas as pd
from datetime import datetime
import os # We need this to check if files exist

# --- Counter Logic ---
counter_file = "run_counter.txt"

# 1. READ: Try to read the old value from the file
try:
    with open(counter_file, 'r') as f:
        # Read the text and convert it to an integer
        run_number = int(f.read())
        
except FileNotFoundError:
    # If the file doesn't exist, this is the first run.
    run_number = 0

# 2. MODIFY: Increment the counter for THIS run
run_number += 1

# 3. WRITE: Save the new (incremented) value back for next time
with open(counter_file, 'w') as f:
    f.write(str(run_number))
# --- End Counter Logic ---


# --- Binance Logic ---
url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

response = requests.get(url)
data = response.json()

# Add timestamp AND our persistent run number
data["timestamp"] = datetime.now()
data["run"] = run_number  # Assign the number we just loaded/incremented

# Convert to pandas DataFrame
df = pd.DataFrame([data])

# Save to CSV (append if file exists)
csv_file = "btc_prices.csv"
header_exists = os.path.exists(csv_file) # Check if file exists BEFORE writing

df.to_csv(csv_file, mode='a', index=False, header=not header_exists)

print(f"Run {run_number}: Saved data to {csv_file}")