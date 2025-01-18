import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_data(filepath):
    """Loads data from a given filepath (e.g., CSV)."""
    try:
        data = pd.read_csv(filepath)
        return data
    except Exception as e:
        print(f"Error loading data from {filepath}: {e}")
        return None

def preprocess_data(data, target_column='price'):
    """Preprocesses the data, including normalization."""
    if data is None:
        return None
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    
    # Ensure the target column exists
    if target_column not in data.columns:
        print(f"Target column '{target_column}' not found in data.")
        return None

    # Fit and transform the target column
    data[target_column] = scaler.fit_transform(data[target_column].values.reshape(-1, 1))
    
    return data, scaler
