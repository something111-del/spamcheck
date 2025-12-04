from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback

# Debug logging for Vercel
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")

try:
    import joblib
    print("joblib imported successfully")
except ImportError as e:
    print(f"Failed to import joblib: {e}")

try:
    import sklearn
    print(f"scikit-learn version: {sklearn.__version__}")
except ImportError as e:
    print(f"Failed to import scikit-learn: {e}")

# Robust model path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "spam_model.joblib")

print(f"Computed MODEL_PATH: {MODEL_PATH}")

app = Flask(__name__)
CORS(app)

model = None
if not os.path.exists(MODEL_PATH):
    print(f"ERROR: Model not found at {MODEL_PATH}")
    # List contents of parent directory to help debug
    parent_dir = os.path.dirname(os.path.dirname(MODEL_PATH))
    if os.path.exists(parent_dir):
         print(f"Contents of {parent_dir}: {os.listdir(parent_dir)}")
else:
    try:
        print(f"Attempting to load model from {MODEL_PATH}...")
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"CRITICAL ERROR loading model: {e}")
        traceback.print_exc()

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
