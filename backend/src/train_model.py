import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Paths relative to the project root (backend/)
DATA_PATH = os.path.join("data", "spam.csv")
MODEL_DIR = os.path.join("models")
MODEL_PATH = os.path.join(MODEL_DIR, "spam_model.joblib")

def load_dataset():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Please download spam.csv.")

    df = pd.read_csv(DATA_PATH, encoding="latin-1")

    if "Category" in df.columns and "Message" in df.columns:
        df = df[["Category", "Message"]]
        df.columns = ["label", "text"]
    elif "v1" in df.columns and "v2" in df.columns:
        df = df[["v1", "v2"]]
        df.columns = ["label", "text"]
    else:
        raise Exception("Unexpected CSV format.")

    df["label"] = df["label"].str.lower().str.strip()
    df = df[df["label"].isin(["spam", "ham"])]
    df.dropna(inplace=True)

    return df

def main():
    print("Loading dataset...")
    try:
        df = load_dataset()
    except Exception as e:
        print(e)
        return

    X = df["text"].values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(sublinear_tf=True)),
        ("clf", LinearSVC())
    ])

    # Define parameter grid for tuning
    param_grid = {
        'tfidf__ngram_range': [(1, 2), (1, 3)],  # Try up to 3-grams for phrases like "gift card"
        'clf__C': [0.1, 1, 10]
    }

    print("Tuning model with GridSearchCV (this may take a moment)...")
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)

    print(f"Best parameters found: {grid_search.best_params_}")
    best_model = grid_search.best_estimator_

    print("Evaluating best model...")
    preds = best_model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, preds))

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    print(f"Best model saved to {MODEL_PATH}")

if __name__ == "__main__":
    main()
