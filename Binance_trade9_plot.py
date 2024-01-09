import logging
import sys
from binance.client import Client
from datetime import datetime
import time
import matplotlib.pyplot as plt
from BinanceKeys import API_K, API_S

# Configure the logging module to write to a log file
#Update logging to include time information and bot version
logging.basicConfig(filename='error_binance_trade9_plot.txt',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  

def log_exception(ex_type, ex_value, ex_traceback):
    """Log unhandled exceptions."""
    logging.error("An unhandled exception occurred:", exc_info=(ex_type, ex_value, ex_traceback))

# Register the custom exception handler
sys.excepthook = log_exception

# API key and secret
api_key = API_K
api_secret = API_S

# Initialize the Binance client
client = Client(api_key, api_secret)

# Ticker and open and close
symbol = "MDTUSDT"
print(f"Below is the opening and closing prices for {symbol}:")
interval = Client.KLINE_INTERVAL_15MINUTE  # 15-minute chart
limit = 100  # Updated number of candlesticks to fetch to 1 day ~100

# Retrieve historical Kline data
klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)

# Iterate through each data point and convert timestamps
#Modify this to a while loop to get live data- DONE
for interval_data in klines:
    start_time = datetime.utcfromtimestamp(interval_data[0] / 1000.0)
    end_time = datetime.utcfromtimestamp(float(interval_data[4]) / 1000.0)

    print(f"Interval: {start_time} to {end_time}")
    print(f"Open: {interval_data[1]}, Close {interval_data[4]}")
    print("-----End of Interval-----")

print('\n')
# Create lists to store timestamps and closing prices
timestamps = [int(entry[0]) for entry in klines]
opening_prices = [float(entry[1]) for entry in klines]
closing_prices = [float(entry[4]) for entry in klines]


# Convert timestamps to human-readable dates
dates = [datetime.utcfromtimestamp(timestamp / 1000.0) for timestamp in timestamps]

# Create a line chart
plt.figure(figsize=(10, 5))
plt.plot(dates, closing_prices, marker='o', linestyle='-')
plt.title(f'{symbol} {interval} Interval Price Chart')
plt.xlabel('Time')
plt.ylabel('Price (USDT)')
plt.grid(True)
#Enable interactive mode so script continues to run
plt.ion()

while True:
    
        # Extract closing prices
        klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)

        # Get the latest closing price from the most recent data point
        latest_closing_price = float(klines[-1][4])

        # Extract closing prices and timestamps
        timestamps = [int(entry[0]) for entry in klines]
        closing_prices = [float(entry[4]) for entry in klines]
        dates = [datetime.utcfromtimestamp(timestamp / 1000.0) for timestamp in timestamps]

        # Update the line chart with the new data
        plt.clf()  # Clear the previous chart
        plt.plot(dates, closing_prices, marker='o', linestyle='-')
        plt.pause(902)  # 15 minute pause for 15minute chart
        
#Ctrl + Alt + M to stop code