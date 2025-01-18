import pandas as pd
import numpy as np
import os
from src.model_manager import ModelManager
from src.sentiment_analyzer import SentimentAnalyzer
from src.data_loader import DataLoader
from src.metrics_manager import MetricsManager
from src.historical_data_manager import HistoricalDataManager
import requests
from sklearn.preprocessing import MinMaxScaler
import joblib

class PredictionEngine:
    def __init__(self, data_loader: DataLoader, model_manager: ModelManager, sentiment_analyzer: SentimentAnalyzer, metrics_manager: MetricsManager, historical_data_manager: HistoricalDataManager):
        self.data_loader = data_loader
        self.model_manager = model_manager
        self.sentiment_analyzer = sentiment_analyzer
        self.metrics_manager = metrics_manager
        self.historical_data_manager = historical_data_manager
        self.models = {}
        self.scalers = {}

    def predict(self, asset, horizon):
        # Load model and scaler if not already loaded
        if asset not in self.models:
            self.models[asset] = self.model_manager.load_model(asset)
            self.scalers[asset] = self.model_manager.load_scaler(asset)

        # Check if model and scaler are loaded successfully
        if self.models[asset] is None or self.scalers[asset] is None:
            print(f"Model or scaler for {asset} not loaded. Prediction failed.")
            return None

        # Get the latest data for the asset
        data = self.get_latest_data(asset)
        if data is None:
            return None

        # Preprocess data
        processed_data = self.preprocess_data(data, self.scalers[asset])
        if processed_data is None:
            return None
        
        processed_data = processed_data.reshape((1, processed_data.shape[0], 1))

        # Make prediction using the loaded model
        model = self.models[asset]
        try:
            prediction = model.predict(processed_data)
        except Exception as e:
            print(f"Error during model prediction: {e}")
            return None

        # Inverse transform to get the actual value
        prediction = self.scalers[asset].inverse_transform(prediction)

        return prediction[0][0]  # Return the prediction value

    def get_historical_predictions(self, asset):
        return self.historical_data_manager.load_historical_predictions(asset)


    def get_latest_metrics(self):
        return self.metrics_manager.get_latest_metrics()

    def get_current_sentiment(self, asset):
        return self.sentiment_analyzer.get_current_sentiment(asset)
    
    def get_latest_data(self, asset):
        # Fetch the latest available data, e.g., last 60 days
        # You might need to adjust the logic based on your data availability
        end_block = self.data_loader.w3.eth.block_number
        start_block = end_block - 500  # Roughly last 1 day, adjust as needed

        data = self.data_loader.load_data(asset, start_block, end_block)

        if data is None or data.empty:
            print(f"Could not fetch latest data for {asset}")
            return None

        return data
    
    def preprocess_data(self, data, scaler):
        # Placeholder for actual data preprocessing logic
        # You would normalize/standardize the data, handle missing values, etc.
        # Example: Scale the 'price' column using the provided scaler
        if data is not None and not data.empty:
            # Ensure the data has the correct shape for scaling
            data = data[['price']].values

            scaled_data = scaler.transform(data)
            return scaled_data
        else:
            print("Data is None or empty, cannot preprocess.")
            return None
