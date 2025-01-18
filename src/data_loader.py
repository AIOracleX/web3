import requests
import pandas as pd
from web3 import Web3, HTTPProvider
import os

class DataLoader:
    def __init__(self, alchemy_url=None):
        self.alchemy_url = alchemy_url or os.getenv('ALCHEMY_URL')
        self.w3 = Web3(HTTPProvider(self.alchemy_url)) if self.alchemy_url else None

    def load_data(self, asset, from_block, to_block):
        # Try fetching from external provider first
        data = self.fetch_data_from_provider(asset, from_block, to_block)

        # If external provider fails or returns no data, try fetching from DEX
        if data is None or data.empty:
            print("Falling back to DEX data since external provider failed or returned no data.")
            data = self.fetch_historical_prices_from_dex(asset, from_block, to_block)
        else:
            print("Successfully fetched data from external provider.")

        return data
    
    def fetch_historical_prices_from_dex(self, asset, from_block, to_block):
        """Fetches historical price data for a given asset from a DEX."""
        if not self.w3.is_connected():
            print("Error: Not connected to Ethereum network.")
            return None
        print("Connected to the BlockChain")
        # Replace with actual logic to fetch historical prices from a DEX
        # This is a placeholder function
        return pd.DataFrame()

    def fetch_data_from_provider(self, asset, start_block, end_block):
        """Fetches historical price data for a given asset from an external data provider."""
        # Example endpoint - replace with your actual provider's endpoint
        url = f"https://api.example.com/historical_prices?asset={asset}&start={start_block}&end={end_block}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Assuming the response is a list of dictionaries with 'timestamp' and 'price' keys
            data = response.json()

            # Convert to DataFrame
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)

            return df

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from provider: {e}")
            return None
