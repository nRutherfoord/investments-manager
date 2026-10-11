# def get_instrumentId_fromTickerSymbol(symbol):
#     print(f"Getting instrument ID for symbol: {symbol}")
#     load_dotenv(Path(__file__).resolve().parent.parent / ".env")
#     url = "https://public-api.etoro.com/api/v1/market-data/search"
#     # Use internalSymbolFull to filter specifically for the symbol
#     params = {
#         "internalSymbolFull": symbol
#     }
    
#     headers = {
#         "x-api-key": os.environ.get("ETORO_PUBLIC_KEY"),
#         "x-user-key": os.environ.get("ETORO_PRIVATE_KEY"),
#         "x-request-id": str(uuid.uuid4())
#     }

#     response = requests.get(url, headers=headers, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         # Find the exact match in the returned items list
#         instrument = next((item for item in data['items'] if item['internalSymbolFull'] == symbol), None)
        
#         if instrument:
#             print(f"Instrument ID: {instrument['instrumentId']}")
#             return instrument['instrumentId']
#         else:
#             print("Instrument not found")
#     else:
#         print(f"Error: {response.status_code}")
        
        

# def get_price_candles_for_instrument(instrument_id, interval, from_date, to_date):
#     url = f"https://public-api.etoro.com/api/v1/market-data/instruments/{instrument_id}/price-candles"
    
#     params = {
#         "interval": interval,
#         "from": from_date,
#         "to": to_date
#     }
    
    
#     headers = {
#         "x-api-key": os.environ.get("ETORO_PUBLIC_KEY"),
#         "x-user-key": os.environ.get("ETORO_PRIVATE_KEY"),
#         "x-request-id": str(uuid.uuid4())
#     }

#     response = requests.get(url, headers=headers, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#     else:
#         print(f"Error: {response.status_code}")