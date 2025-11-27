# backend/ai_core/synthetic_data.py
import numpy as np
import pandas as pd
from .risk_features import feature_list

def generate_synthetic(n=4000, random_state=42):
    """
    Generate a balanced-ish synthetic investor dataset.
    Columns: age, income, tolerance, horizon_years, volatility_pref, label
    """
    rng = np.random.default_rng(random_state)
    ages = rng.integers(21, 65, size=n)
    incomes = rng.normal(100000, 30000, size=n).clip(20000, 500000)
    tolerance = rng.uniform(0, 1, size=n)  # 0=low,1=high
    horizon_years = rng.integers(1, 30, size=n)
    volatility_pref = rng.uniform(0, 1, size=n)

    # Score heuristic (simple interpretable rule)
    score = (
        (1 - (ages - 21) / 44) * 0.25 +
        (incomes / 500000) * 0.25 +
        tolerance * 0.3 +
        (horizon_years / 30) * 0.1 +
        volatility_pref * 0.1
    )

    labels = np.where(score < 0.4, "Conservative", np.where(score < 0.7, "Moderate", "Aggressive"))

    df = pd.DataFrame({
        "age": ages,
        "income": incomes,
        "tolerance": tolerance,
        "horizon_years": horizon_years,
        "volatility_pref": volatility_pref,
        "label": labels
    })

    # ensure features ordering
    cols = feature_list()
    return df[cols + ["label"]]
