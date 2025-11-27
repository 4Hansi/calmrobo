# backend/risk_classifier.py

import os
import joblib
from .ai_core.risk_features import ensure_feature_order

model_path = os.path.join(os.path.dirname(__file__), "models", "risk_classifier.pkl")

# Load model if available
USE_MODEL = os.path.exists(model_path)
if USE_MODEL:
    model_obj = joblib.load(model_path)
    rf_model = model_obj["model"]
    feature_order = model_obj["features"]


def simple_rule_classifier(features):
    """Fallback rule-based risk classification."""
    age = features.get("age")
    tolerance = (features.get("tolerance") or "").lower()
    horizon = features.get("horizon_years")

    # Tolerance is the strongest signal
    if "high" in tolerance or "aggressive" in tolerance:
        return "aggressive"
    if "medium" in tolerance or "moderate" in tolerance:
        return "moderate"
    if "low" in tolerance or "conservative" in tolerance:
        return "conservative"

    # Age-based signals
    if age is not None:
        if age < 30:
            return "aggressive"
        if age < 45:
            return "moderate"

    # Horizon signals
    if horizon:
        if horizon > 10:
            return "aggressive"
        if horizon > 5:
            return "moderate"

    return "conservative"


def predict_risk_profile(features_dict):
    """Hybrid ML + rule-based classifier."""

    # ML works only if model exists AND all fields present
    if USE_MODEL and all(k in features_dict for k in feature_order):
        try:
            arr = ensure_feature_order(features_dict, feature_order)
            ml_pred = rf_model.predict([arr])[0]
            return ml_pred
        except Exception:
            pass  # fall back to rule-based

    # Fallback rule classifier
    return simple_rule_classifier(features_dict)
