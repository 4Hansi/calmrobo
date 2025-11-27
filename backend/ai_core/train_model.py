# backend/ai_core/train_model.py
import os
import joblib
import argparse
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from ..ai_core.synthetic_data import generate_synthetic
from ..ai_core.risk_features import feature_list

def train_and_save_model(models_dir="..\\models", random_state=42, n_estimators=200):
    """
    Train RandomForest on synthetic data and save to backend/models/risk_classifier.pkl
    - models_dir: relative to this script (ai_core/)
    """
    print("Generating synthetic data...")
    df = generate_synthetic(n=4000, random_state=random_state)
    X = df[feature_list()].values
    y = df["label"].values

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=random_state)

    print("Training RandomForest (this may take a few seconds)...")
    rf = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1, random_state=random_state)
    rf.fit(X_train, y_train)

    print("Evaluating...")
    y_pred = rf.predict(X_test)
    print(classification_report(y_test, y_pred))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    # save model + feature order
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_models_dir = os.path.normpath(os.path.join(script_dir, models_dir))
    os.makedirs(target_models_dir, exist_ok=True)
    model_filepath = os.path.join(target_models_dir, "risk_classifier.pkl")
    joblib.dump({"model": rf, "features": feature_list()}, model_filepath)
    print(f"Model saved to: {os.path.abspath(model_filepath)}")


if __name__ == "__main__":
    # allow running: python backend/ai_core/train_model.py
    train_and_save_model()
