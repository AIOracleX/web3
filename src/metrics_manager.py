import pandas as pd
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

class MetricsManager:
    def __init__(self, metrics_dir='metrics'):
        self.metrics_dir = metrics_dir
        os.makedirs(self.metrics_dir, exist_ok=True)

    def calculate_metrics(self, y_true, y_pred):
        """Calculates MAE and RMSE."""
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return mae, rmse

    def save_metrics(self, asset, mae, rmse):
        """Saves metrics to a CSV file."""
        timestamp = pd.Timestamp.now()
        metrics_file = os.path.join(self.metrics_dir, 'metrics.csv')

        # Create DataFrame if file doesn't exist
        if not os.path.exists(metrics_file):
            df = pd.DataFrame(columns=['timestamp', 'asset', 'mae', 'rmse'])
        else:
            df = pd.read_csv(metrics_file)

        # Append new metrics
        new_row = pd.DataFrame([{'timestamp': timestamp, 'asset': asset, 'mae': mae, 'rmse': rmse}])
        df = pd.concat([df, new_row], ignore_index=True)

        # Save to CSV
        df.to_csv(metrics_file, index=False)

    def load_metrics(self, asset=None):
        """Loads metrics from a CSV file, optionally filtering by asset."""
        metrics_file = os.path.join(self.metrics_dir, 'metrics.csv')

        if not os.path.exists(metrics_file):
            print("Metrics file not found.")
            return None

        df = pd.read_csv(metrics_file)

        if asset:
            df = df[df['asset'] == asset]

        return df

    def get_latest_metrics(self):
        """Returns the latest metrics for each asset."""
        metrics_file = os.path.join(self.metrics_dir, 'metrics.csv')

        if not os.path.exists(metrics_file):
            print("Metrics file not found.")
            return None

        df = pd.read_csv(metrics_file)
        
        if df.empty:
            return {'metrics': []}
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Get the latest timestamp for each asset
        latest_metrics = df.groupby('asset').apply(lambda x: x.loc[x['timestamp'].idxmax()])

        return {
            'metrics': latest_metrics.drop(columns='timestamp', errors='ignore').to_dict('records')
        }
