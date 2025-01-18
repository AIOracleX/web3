import tensorflow as tf
import joblib
import os

def load_model(asset):
    model_path = os.path.join('models', f'{asset}_model.h5')
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        print(f"Error loading model for {asset}: {e}")
        return None

def load_scaler(asset):
    scaler_path = os.path.join('models', f'{asset}_scaler.pkl')
    try:
        scaler = joblib.load(scaler_path)
        return scaler
    except Exception as e:
        print(f"Error loading scaler for {asset}: {e}")
        return None
