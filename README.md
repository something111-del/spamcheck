# SpamCheck - SMS Spam Detection System

SpamCheck is a full-stack machine learning application designed to classify SMS messages as either "Spam" or "Ham" (safe). It features a Flask REST API backend and a modern, responsive frontend.

##  Key Features
- **Real-time Prediction**: Instantly classify SMS messages.
- **Batch Processing**: Support for analyzing multiple messages at once.
- **Robust Model**: Tuned machine learning model for high accuracy.
- **Dockerized**: Ready for containerized deployment.

##  Model Improvements & Efficiency
We significantly enhanced the initial model to better detect subtle spam patterns, such as "coupons", "gift cards", and promotional offers.

### Evolution
1.  **Baseline**: Initially used a standard Naive Bayes and simple LinearSVC model.
2.  **Optimization**: We upgraded to a **LinearSVC** pipeline with **TF-IDF** vectorization.
3.  **Hyperparameter Tuning**:
    -   **GridSearchCV**: Implemented to automatically find the optimal `C` parameter for the SVM.
    -   **N-Gram Expansion**: Expanded TF-IDF to use **(1, 3) n-grams**. This allows the model to learn phrases (e.g., "free gift card", "claim your prize") rather than just individual words.

### Results
These changes led to a measurable increase in **F1-Score** and **Recall** for the "Spam" class. The model is now much more efficient at catching previously missed spam messages without increasing false positives.

##  Tech Stack
-   **Backend**: Python, Flask, Scikit-learn, Pandas, Joblib
-   **Frontend**: HTML5, CSS3, JavaScript (Fetch API)
-   **Deployment**: Docker, Gunicorn

## Setup & Installation

### Prerequisites
-   Python 3.10+
-   Docker (Optional)

### 1. Local Setup
```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the model (Required for first run)
python src/train_model.py

# 5. Start the API
python src/api.py
```
The API will run at `http://127.0.0.1:8000`.

### 2. Frontend
Simply open `frontend/index.html` in your web browser to use the interface.

### 3. Docker Setup
```bash
cd backend
docker build -t spamcheck-api .
docker run -p 8000:8000 spamcheck-api
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API Welcome message |
| `GET` | `/health` | Check API status |
| `POST` | `/predict` | Predict single message. Body: `{"text": "message"}` |
| `POST` | `/batch-predict` | Predict multiple. Body: `{"messages": ["msg1", "msg2"]}` |
