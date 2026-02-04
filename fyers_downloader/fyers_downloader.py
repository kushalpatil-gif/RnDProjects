import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_BASE = 'https://api.fyers.in'  # base URL for Fyers API
ACCESS_TOKEN = os.getenv('FYERS_ACCESS_TOKEN')

HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# Example function to get historical data for a symbol
def fetch_historical(symbol, resolution='D', date_from=None, date_to=None):
    """Fetch historical data for a symbol.
    symbol: exchange:token format used by Fyers (e.g., NSE:RELIANCE-EQ)
    resolution: D (daily), 1 (1min), etc.
    date_from/date_to: YYYY-MM-DD strings
    """
    if date_from is None:
        date_from = (datetime.now()).strftime('%Y-%m-%d')
    if date_to is None:
        date_to = (datetime.now()).strftime('%Y-%m-%d')

    endpoint = f"{API_BASE}/api/v2/history"
    params = {
        'symbol': symbol,
        'resolution': resolution,
        'date_from': date_from,
        'date_to': date_to
    }
    resp = requests.get(endpoint, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def save_to_csv(data, out_path):
    df = pd.DataFrame(data)
    df.to_csv(out_path, index=False)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', required=True, help='Symbol in Fyers format, e.g., NSE:RELIANCE-EQ')
    parser.add_argument('--from', dest='date_from', help='Start date YYYY-MM-DD')
    parser.add_argument('--to', dest='date_to', help='End date YYYY-MM-DD')
    parser.add_argument('--out', dest='out', default='output.csv')
    args = parser.parse_args()

    if not ACCESS_TOKEN:
        print('Please set FYERS_ACCESS_TOKEN environment variable.')
        exit(1)

    data = fetch_historical(args.symbol, date_from=args.date_from, date_to=args.date_to)
    # Fyers response shape may vary; try to find OHLC data
    if 'candles' in data:
        # candles is list of [time, open, high, low, close, volume]
        candles = data['candles']
        df = pd.DataFrame(candles, columns=['timestamp','open','high','low','close','volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.to_csv(args.out, index=False)
        print(f'Saved to {args.out}')
    else:
        print('Unexpected response format:', data)

