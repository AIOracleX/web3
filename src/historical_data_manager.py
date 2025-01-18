import pandas as pd
import os

class HistoricalDataManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def save_historical_predictions(self, asset, predictions):
        """Saves historical predictions to a CSV file."""
        timestamp = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
        file_path = os.path.join(self.data_dir, f'{asset}_historical_predictions_{timestamp}.csv')

        try:
            # Assuming 'predictions' is a list of dictionaries
            df = pd.DataFrame(predictions)
            df.to_csv(file_path, index=False)
            print(f"Historical predictions for {asset} saved to {file_path}")
        except Exception as e:
            print(f"Error saving historical predictions for {asset}: {e}")

    def load_historical_predictions(self, asset):
        """Loads historical predictions for a given asset."""
        # Find all files for the asset
        files = [f for f in os.listdir(self.data_dir) if f.startswith(f'{asset}_historical_predictions_') and f.endswith('.csv')]
        if not files:
            print(f"No historical predictions found for {asset}")
            return None

        # Sort files by timestamp (newest first)
        files.sort(reverse=True)

        # Load the most recent file
        latest_file = files[0]
        file_path = os.path.join(self.data_dir, latest_file)

        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            print(f"Error loading historical predictions for {asset}: {e}")
            return None
