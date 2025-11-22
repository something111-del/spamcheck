from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

# Ensure we look for models relative to the backend directory if run from there
# or handle the path correctly.
# User provided: MODEL_PATH = os.path.join("models", "spam_model.joblib")
# This assumes running from backend/
MODEL_PATH = os.path.join("models", "spam_model.joblib")

app = Flask(__name__)
CORS(app)

if not os.path.exists(MODEL_PATH):
    # Fallback for robustness if run from src/
    if os.path.exists(os.path.join("..", "models", "spam_model.joblib")):
        MODEL_PATH = os.path.join("..", "models", "spam_model.joblib")
    else:
        # We'll just print a warning instead of raising error immediately to let app start
        print("Warning: Model not found at", MODEL_PATH)

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/")
def home():
    return jsonify({"message": "SpamCheck API is running. Use /predict to classify SMS."}), 200

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text'"}), 400

    text = data["text"]
    if model:
        pred = model.predict([text])[0]
        return jsonify({"prediction": pred}), 200
    else:
        return jsonify({"error": "Model not loaded"}), 500

@app.route("/batch-predict", methods=["POST"])
def batch_predict():
    data = request.get_json()
    # Fixed bug: "messages" in [] -> "messages" not in data
    if not data or "messages" not in data:
        return jsonify({"error": "Missing 'messages'"}), 400

    msgs = data["messages"]
    if model:
        preds = model.predict(msgs).tolist()
        return jsonify({"predictions": preds}), 200
    else:
        return jsonify({"error": "Model not loaded"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
