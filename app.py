from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from src.prediction_engine import PredictionEngine

load_dotenv()

app = Flask(__name__)
prediction_engine = PredictionEngine()

@app.route('/predictions/<asset>', methods=['GET'])
def get_predictions(asset):
    try:
        horizon = request.args.get('horizon', default=1, type=int)
        prediction = prediction_engine.predict(asset, horizon)
        if prediction:
            return jsonify({'asset': asset, 'horizon': horizon, 'prediction': prediction})
        else:
            return jsonify({'error': 'Asset not found or prediction failed'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predictions/<asset>/history', methods=['GET'])
def get_history(asset):
    try:
        history = prediction_engine.get_historical_predictions(asset)
        if history:
            return jsonify(history)
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
