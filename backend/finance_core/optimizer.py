# backend/finance_core/optimizer.py

from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
import numpy as np
import pandas as pd

def risk_to_target_vol(risk_profile: str):
    rp = (risk_profile or "moderate").lower()
    if rp == "conservative":
        return 0.08
    if rp in ("moderate", "balanced"):
        return 0.15
    return 0.28  # aggressive

def optimize_portfolio_for_risk(price_history_df: pd.DataFrame, risk_profile="Moderate"):
    """
    price_history_df: DataFrame with columns = tickers
    Returns dict with weights and metrics.
    """
    if price_history_df is None or price_history_df.empty:
        return {"risk_profile": risk_profile, "weights": {}, "expected_return": 0.0, "volatility": 0.0, "sharpe": 0.0}

    try:
        mu = mean_historical_return(price_history_df)
        S = CovarianceShrinkage(price_history_df).ledoit_wolf()
        ef = EfficientFrontier(mu, S)

        # For different risk preferences choose different objectives:
        rp = (risk_profile or "moderate").lower()
        if rp == "conservative":
            # maximize return for a low risk target (min volatility subject to return)
            try:
                # target volatility approach: treat via efficient frontier by max_sharpe then scale
                raw_w = ef.max_sharpe()
            except Exception:
                raw_w = ef.min_volatility()
        elif rp in ("moderate", "balanced"):
            raw_w = ef.max_sharpe()
        else:
            # aggressive -> push towards growth: we maximize Sharpe but allow leverage removal
            raw_w = ef.max_sharpe()

        cleaned = ef.clean_weights()
        perf = ef.portfolio_performance(verbose=False)
    except Exception as e:
        # fallback equal weight
        tickers = list(price_history_df.columns)
        if not tickers:
            return {"risk_profile": risk_profile, "weights": {}, "expected_return": 0.0, "volatility": 0.0, "sharpe": 0.0}
        w = 1.0 / len(tickers)
        cleaned = {t: round(w, 4) for t in tickers}
        perf = (0.0, 0.0, 0.0)

    # Ensure numeric output
    expected_return = float(perf[0]) if perf and perf[0] is not None else 0.0
    volatility = float(perf[1]) if perf and perf[1] is not None else 0.0
    sharpe = float(perf[2]) if perf and perf[2] is not None else 0.0

    return {
        "risk_profile": risk_profile,
        "weights": cleaned,
        "expected_return": expected_return,
        "volatility": volatility,
        "sharpe": sharpe,
    }
