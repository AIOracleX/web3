import pandas as pd
import os
import sys
from datetime import datetime

# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = 'data'

def main():
    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    data_loader = DataLoader()

    # Example: Fetch data for a specific asset and date range
    asset_name = 'ETH'  # Example asset
    from_block = 18000000  # Replace with your desired start block
    to_block = 18000500  # Replace with your desired end block

    data = data_loader.load_data(asset_name, from_block, to_block)
    
    if data is not None:
        # Add a timestamp to the filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(DATA_DIR, f'{asset_name}_data_{timestamp}.csv')
        
        # Save the data to a CSV file
        data.to_csv(file_path)
        print(f"Data saved to {file_path}")
    else:
        print("Could not fetch data.")

if __name__ == "__main__":
    main()
