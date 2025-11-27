# backend/finance_core/market_data.py

import yfinance as yf
import pandas as pd
from typing import List

def get_latest_quotes(tickers: List[str]):
    quotes = {}
    for t in tickers:
        try:
            info = yf.Ticker(t).history(period="1d")
            if not info.empty:
                last = float(info["Close"].iloc[-1])
                quotes[t] = {"last": last}
            else:
                quotes[t] = {"last": None}
        except Exception:
            quotes[t] = {"last": None}
    return quotes

def get_price_history(tickers, period="1y"):
    """
    Return DataFrame with columns=tickers and rows=dates of Close prices.
    If multiple tickers are provided, use yf.download; if a single ticker,
    we still return a DataFrame.
    """
    if not tickers:
        return pd.DataFrame()

    # yfinance accepts space/comma-separated tickers
    # ensure list -> string
    if isinstance(tickers, (list, tuple)):
        tickers_str = " ".join(tickers)
    else:
        tickers_str = str(tickers)

    try:
        df = yf.download(tickers_str, period=period, progress=False)["Close"]
    except Exception:
        # final fallback: try per-ticker download
        frames = []
        for t in (tickers if isinstance(tickers, (list, tuple)) else [tickers]):
            try:
                single = yf.Ticker(t).history(period=period)
                if single is not None and not single.empty:
                    frames.append(single["Close"].rename(t))
            except Exception:
                continue
        if not frames:
            return pd.DataFrame()
        return pd.concat(frames, axis=1).dropna()

    # If df is a Series (single ticker), convert to DataFrame
    if isinstance(df, pd.Series):
        df = df.to_frame(name=tickers if isinstance(tickers, str) else tickers[0])

    # if df has columns for tickers, drop any columns that are all NaN
    if isinstance(df, pd.DataFrame):
        df = df.dropna(axis=1, how="all")
        # if after dropna there's no columns, return empty df
        if df.empty:
            return pd.DataFrame()

    return df
