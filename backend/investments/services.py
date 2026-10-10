import os
import uuid
from pathlib import Path

import requests
from dotenv import load_dotenv


def get_instrumentId_fromTickerSymbol(symbol):
    print(f"Getting instrument ID for symbol: {symbol}")
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    url = "https://public-api.etoro.com/api/v1/market-data/search"
    # Use internalSymbolFull to filter specifically for the symbol
    params = {
        "internalSymbolFull": symbol
    }
    
    headers = {
        "x-api-key": os.environ.get("ETORO_PUBLIC_KEY"),
        "x-user-key": os.environ.get("ETORO_PRIVATE_KEY"),
        "x-request-id": str(uuid.uuid4())
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        # Find the exact match in the returned items list
        instrument = next((item for item in data['items'] if item['internalSymbolFull'] == symbol), None)
        
        if instrument:
            print(f"Instrument ID: {instrument['instrumentId']}")
            return instrument['instrumentId']
        else:
            print("Instrument not found")
    else:
        print(f"Error: {response.status_code}")
        
        

def get_price_candles_for_instrument(instrument_id, interval, from_date, to_date):
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    url = f"https://public-api.etoro.com/api/v1/market-data/instruments/{instrument_id}/price-candles"
    
    params = {
        "interval": interval,
        "from": from_date,
        "to": to_date
    }
    
    headers = {
        "x-api-key": os.environ.get("ETORO_PUBLIC_KEY"),
        "x-user-key": os.environ.get("ETORO_PRIVATE_KEY"),
        "x-request-id": str(uuid.uuid4())
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code}")
        
        
        
def get_total_invested ():

    url = "https://public-api.etoro.com/api/v1/trading/info/demo/pnl"

    headers = {
        "x-api-key": os.environ.get("ETORO_PUBLIC_KEY"),
        "x-user-key": os.environ.get("ETORO_PRIVATE_KEY"),
        "x-request-id": str(uuid.uuid4())
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        # Sum all position amounts
        positions_amount = sum(pos['amount'] for pos in data['positions'])
        
        # Sum all mirror position amounts and adjusted available amounts
        mirrors_positions_amount = sum(
            pos['amount'] 
            for mirror in data['mirrors'] 
            for pos in mirror['positions']
        )
        mirrors_adjusted_amount = sum(
            mirror['availableAmount'] - mirror['closedPositionsNetProfit']
            for mirror in data['mirrors']
        )
        
        # Sum manual pending orders (mirrorID = 0)
        orders_for_open_amount = sum(
            order['amount'] 
            for order in data['ordersForOpen'] 
            if order['mirrorID'] == 0
        )
        
        # Sum all orders
        orders_amount = sum(order['amount'] for order in data['orders'])
        
        # Sum external costs for manual pending orders
        external_costs = sum(
            order['totalExternalCosts'] 
            for order in data['ordersForOpen'] 
            if order['mirrorID'] == 0
        )
        
        total_invested = (positions_amount + mirrors_positions_amount + mirrors_adjusted_amount 
                        + orders_for_open_amount + orders_amount + external_costs)
        
        print(f"Total Invested: {total_invested}")
    else:
        print(f"Error: {response.status_code}")
    