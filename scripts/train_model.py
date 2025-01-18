import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib
import os
import sys
# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader
from src.model_manager import ModelManager
from src.metrics_manager import MetricsManager
from dotenv import load_dotenv

load_dotenv()
# Assuming you have preprocessed data in a CSV
DATA_PATH = 'data/preprocessed_data.csv'
MODEL_DIR = 'models'

def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

def train_model(asset_name, data, model_manager, metrics_manager):
    # Preprocess data: normalization
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # Split data into training and testing sets
    train_size = int(len(scaled_data) * 0.67)
    test_size = len(scaled_data) - train_size
    train, test = scaled_data[0:train_size,:], scaled_data[train_size:len(scaled_data),:]

    # Prepare the dataset with look_back (e.g., 60 previous prices)
    look_back = 60
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)

    # Reshape input to be [samples, time steps, features] for LSTM
    trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
    testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))

    # Create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(50, input_shape=(look_back, 1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=1, batch_size=1, verbose=2)

    # Save the model
    model_manager.save_model(asset_name, model)
    
    # Save the scaler
    scaler_filename = f"{asset_name}_scaler.pkl"
    scaler_path = os.path.join(MODEL_DIR, scaler_filename)
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}")

    # Evaluate the model
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)

    # Invert predictions to original scale
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform([testY])

    # Calculate metrics
    mae, rmse = metrics_manager.calculate_metrics(testY[0], testPredict[:,0])
    metrics_manager.save_metrics(asset_name, mae, rmse)

    print(f'Test MAE: {mae}, Test RMSE: {rmse}')
    return model, scaler


def main():
    # Ensure the model directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)

    data_loader = DataLoader()
    model_manager = ModelManager()
    metrics_manager = MetricsManager()

    # Example: Fetch data for a specific asset and date range
    asset_name = 'ETH'  # Example asset
    from_block = 18000000  # Replace with your desired start block
    to_block = 18000500  # Replace with your desired end block
    #data = data_loader.fetch_data_from_provider(asset_name, from_block, to_block)
    data = data_loader.load_data(asset_name, from_block, to_block)

    if data is not None and not data.empty:
        # Select only 'price' column for training
        price_data = data[['price']].values  # Use double brackets to keep the DataFrame structure

        # Train the model on the 'price' data
        train_model(asset_name, price_data, model_manager, metrics_manager)
    else:
        print("Could not fetch data for training.")

if __name__ == "__main__":
    main()
