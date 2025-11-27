# backend/portfolio.py

import re
from .finance_core.market_data import get_price_history
from .finance_core.optimizer import optimize_portfolio_for_risk

# Default US tech basket (fallback)
DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA"]

# Name → ticker mapping (US + India)
NAME_TO_TICKER = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOG",
    "alphabet": "GOOG",
    "amazon": "AMZN",
    "tesla": "TSLA",

    # India
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
    "reliance": "RELIANCE.NS",
    "hdfc": "HDFCBANK.NS",
    "hdfc bank": "HDFCBANK.NS",
    "itc": "ITC.NS",
    "yes bank": "YESBANK.NS",
}

# Regex for uppercase tokens (tickers)
TICKER_REGEX = re.compile(r"\b[A-Z]{1,6}(?:\.[A-Z]{1,4}|-[A-Z]{2,4})?\b")

# Regex for explicit "tickers: X, Y"
COMMA_SEP_REGEX = re.compile(r"tickers?\s*[:=]\s*(.+)$", re.IGNORECASE)


def normalize_ticker(t: str):
    return t.strip().upper()


def extract_tickers_from_text(text: str):
    """
    Parse user-provided tickers or company names.
    Strategy:
    1. If "tickers: AAPL, TCS.NS" → parse explicitly
    2. If user typed uppercase codes → detect automatically
    3. If user typed company name → map via NAME_TO_TICKER
    """
    if not text or not isinstance(text, str):
        return []

    # 1 — explicit list
    m = COMMA_SEP_REGEX.search(text)
    if m:
        raw = m.group(1)
        parts = [p.strip() for p in re.split(r"[,\s]+", raw) if p.strip()]
        out = []
        for p in parts:
            if re.match(r"^[A-Za-z0-9.\-]+$", p):
                out.append(normalize_ticker(p))
        return out

    # 2 — uppercase tickers
    candidates = TICKER_REGEX.findall(text)
    if candidates:
        return [normalize_ticker(c) for c in candidates][:10]  # safety cap

    # 3 — company names
    lowered = text.lower()
    found = []
    for name, ticker in NAME_TO_TICKER.items():
        if name in lowered:
            found.append(ticker)

    return list(dict.fromkeys(found))  # dedupe, preserve order


def build_portfolio_for_user(risk_profile, tickers=None):
    """
    Main function: builds the portfolio using chosen tickers or defaults.
    Returns:
    {
      risk_profile: "...",
      weights: {...},
      volatility: ...,
      expected_return: ...,
      sharpe: ...,
      tickers_used: [...]
    }
    """

    # sanitize input
    if tickers:
        if isinstance(tickers, str):
            tickers = [t.strip() for t in re.split(r"[,\s]+", tickers) if t.strip()]
        tickers = [normalize_ticker(t) for t in tickers]
        if not tickers:
            tickers = DEFAULT_TICKERS
    else:
        tickers = DEFAULT_TICKERS

    # Download price history
    history = get_price_history(tickers, "1y")

    # Run optimizer
    portfolio = optimize_portfolio_for_risk(history, risk_profile)

    # Add which tickers were used
    portfolio["tickers_used"] = tickers

    return portfolio
