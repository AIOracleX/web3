import tensorflow as tf
import torch
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from web3 import Web3
import requests
import os
# from src.data_processing import load_data, preprocess_data # You might need additional preprocessing steps
# from src.utils import load_model # And model loading functions

class PredictionEngine:
    def __init__(self):
        self.models = {}  # Store loaded models
        self.scalers = {} # Store scalers for different assets
        self.w3 = Web3(Web3.HTTPProvider(os.environ.get("ALCHEMY_URL")))
        print(f"Connection to Alchemy successful: {not self.w3.is_connected()}")

    def predict(self, asset, horizon):
        # Load model and scaler if not already loaded
        if asset not in self.models:
            self.models[asset] = self.load_model(asset)
            self.scalers[asset] = self.load_scaler(asset)


        # Get data from alchemy
        latest_block = self.w3.eth.block_number
        print(f"Latest block: {latest_block}")

        # Get data
        data = self.load_data(asset, latest_block - 100, latest_block)

        # Preprocess data
        processed_data = self.preprocess_data(data, self.scalers[asset])

        # Make prediction using the loaded model
        model = self.models[asset]
        prediction = model.predict(processed_data)

        # Inverse transform to get the actual value
        prediction = self.scalers[asset].inverse_transform(prediction)

        return prediction[0][0]  # Return the prediction value
    
    def get_historical_predictions(self, asset):
        #Replace with your logic
        return {
            'asset': asset,
            'history': [
                {'timestamp': '2023-01-01', 'prediction': 100, 'actual': 98},
                {'timestamp': '2023-01-02', 'prediction': 102, 'actual': 103},
            ]
        }
    
    def get_latest_metrics(self):
        return {
            'metrics': [
                {'asset': 'ETH', 'mae': 0.5, 'rmse': 0.7, 'timestamp': '2024-01-10'},
                {'asset': 'BTC', 'mae': 0.8, 'rmse': 0.9, 'timestamp': '2024-01-10'},
            ]
        }
    
    def get_current_sentiment(self, asset):
        return {
            'asset': asset,
            'sentiment': {
                'twitter': 0.8,
                'reddit': 0.6,
                'overall': 0.7,
            },
            'timestamp': '2024-01-10'
        }

    def load_model(self, asset):
        model_path = os.path.join('models', f'{asset}_model.h5')

        if not os.path.exists(model_path):
            print(f"Model file for {asset} not found at {model_path}")
            return None

        try:
            model = tf.keras.models.load_model(model_path)
            print(f"Model for {asset} loaded successfully from {model_path}")
            return model
        except Exception as e:
            print(f"Error loading model for {asset} from {model_path}: {e}")
            return None
        
    def load_scaler(self, asset):
        scaler_path = os.path.join('models', f'{asset}_scaler.pkl')

        if not os.path.exists(scaler_path):
            print(f"Scaler file for {asset} not found at {scaler_path}")
            return None

        try:
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)
                print(f"Scaler for {asset} loaded from {scaler_path}")
                return scaler
        except Exception as e:
            print(f"Error loading scaler for {asset} from {scaler_path}: {e}")
            return None
    
    def load_data(self, asset, from_block, to_block):
        # Placeholder for actual data loading logic
        # You would interact with the blockchain, fetch relevant data for the asset,
        # potentially from DEXs or other on-chain sources
        print(f"Fetching data for {asset} from block {from_block} to {to_block}")

        # Replace this with your actual data fetching logic
        # For example, fetching historical prices from a DEX
        # data = self.fetch_historical_prices_from_dex(asset, from_block, to_block)
        # Or fetch data from a data provider
        data = self.fetch_data_from_provider(asset, from_block, to_block)
        print(data)

        return data
    
    def fetch_data_from_provider(self, asset, start_block, end_block):
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
    
    def preprocess_data(self, data, scaler):
        # Placeholder for actual data preprocessing logic
        # You would normalize/standardize the data, handle missing values, etc.

        # Example: Scale the 'price' column using the provided scaler
        if data is not None and not data.empty:
            # Ensure the data has the correct shape for scaling
            if len(data.shape) == 1:
                data = data.values.reshape(-1, 1)
            elif data.shape[1] == 1:
                data = data.values
            else:
                raise ValueError("Data must be a 1D array or a DataFrame with a single column named 'price'")

            scaled_data = scaler.transform(data)
            return scaled_data
        else:
            print("Data is None or empty, cannot preprocess.")
            return None
