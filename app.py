from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.prediction_engine import PredictionEngine
from src.data_loader import DataLoader
from src.model_manager import ModelManager
from src.sentiment_analyzer import SentimentAnalyzer
from src.metrics_manager import MetricsManager
from src.historical_data_manager import HistoricalDataManager

load_dotenv()

app = Flask(__name__)
data_loader = DataLoader()
model_manager = ModelManager()
sentiment_analyzer = SentimentAnalyzer()
metrics_manager = MetricsManager()
historical_data_manager = HistoricalDataManager()
prediction_engine = PredictionEngine(data_loader, model_manager, sentiment_analyzer, metrics_manager, historical_data_manager)

@app.route('/predictions/<asset>', methods=['GET'])
def get_predictions(asset):
    try:
        horizon = request.args.get('horizon', default=1, type=int)
        prediction = prediction_engine.predict(asset, horizon)
        if prediction is not None:  # Check if prediction is a number
            return jsonify({'asset': asset, 'horizon': horizon, 'prediction': prediction})
        else:
            return jsonify({'error': f'Could not generate prediction for {asset}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predictions/<asset>/history', methods=['GET'])
def get_history(asset):
    try:
        history = prediction_engine.get_historical_predictions(asset)
        if history is not None:
            # Convert DataFrame to JSON-serializable format
            history_json = history.to_dict(orient='records')
            return jsonify({'asset': asset, 'history': history_json})
        else:
            return jsonify({'error': 'Asset not found or history unavailable'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/metrics', methods=['GET'])
def get_metrics():
    try:
        metrics = prediction_engine.get_latest_metrics()
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sentiment/<asset>', methods=['GET'])
def get_sentiment(asset):
    try:
        sentiment = prediction_engine.get_current_sentiment(asset)
        return jsonify(sentiment)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
