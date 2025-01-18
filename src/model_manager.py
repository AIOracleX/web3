import tensorflow as tf
import joblib
import os

class ModelManager:
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir

    def load_model(self, asset):
        """Loads a pre-trained model for the given asset."""
        model_path = os.path.join(self.model_dir, f'{asset}_model.h5')
        try:
            model = tf.keras.models.load_model(model_path)
            return model
        except Exception as e:
            print(f"Error loading model for {asset}: {e}")
            return None

    def load_scaler(self, asset):
        """Loads a pre-trained scaler for the given asset."""
        scaler_path = os.path.join(self.model_dir, f'{asset}_scaler.pkl')
        try:
            scaler = joblib.load(scaler_path)
            return scaler
        except Exception as e:
            print(f"Error loading scaler for {asset}: {e}")
            return None
