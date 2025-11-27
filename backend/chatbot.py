# backend/chatbot.py

import os
import json
import cohere
from dotenv import load_dotenv

from .risk_classifier import predict_risk_profile
from .portfolio import build_portfolio_for_user, extract_tickers_from_text
from .finance_core.sentiment_engine import get_sentiment, classify_sentiment

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

REQUIRED_FIELDS = ["age", "income", "tolerance", "horizon_years"]
FRIENDLY_FIELD_NAMES = {
    "age": "your age",
    "income": "your annual income",
    "tolerance": "your risk tolerance (low/medium/high)",
    "horizon_years": "your investment horizon (in years)"
}

class Chatbot:
    def __init__(self):
        self.MODEL = "c4ai-aya-23"

        # Persistent memory for conversation (like ChatGPT)
        self.memory = {
            "age": None,
            "income": None,
            "tolerance": None,
            "horizon_years": None,
            "volatility_pref": None,
            "tickers": None,
        }

    # Extract structured features using Cohere
    def extract_features(self, user_message: str):
        prompt = f"""
        Extract user financial attributes from the message below.
        Return ONLY a JSON object with keys:
        age, income, tolerance, horizon_years, volatility_pref.

        If a field is not mentioned, set it to null.

        USER MESSAGE:
        "{user_message}"
        """
        response = co.chat(model=self.MODEL, message=prompt, temperature=0.2)

        raw = response.text.strip()
        try:
            if raw.startswith("```"):
                raw = raw.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(raw)
        except:
            parsed = {k: None for k in self.memory.keys()}

        return parsed

    # Update memory with only fields the user provided
    def merge_with_memory(self, new_data: dict):
        for key in self.memory:
            if key in new_data and new_data[key] not in [None, "", 0]:
                self.memory[key] = new_data[key]

    def get_missing_fields(self):
        missing = []
        for key in REQUIRED_FIELDS:
            if self.memory.get(key) in [None, "", 0]:
                missing.append(key)
        return missing

    # MAIN CHAT LOGIC
    def chat(self, user_message: str):

        # Detect sentiment
        sentiment = get_sentiment(user_message)
        sentiment_class = classify_sentiment(sentiment["polarity"])

        # Extract user-provided tickers
        tickers = extract_tickers_from_text(user_message)
        if tickers:
            self.memory["tickers"] = tickers

        # Extract structured fields (age, income, tolerance...)
        extracted = self.extract_features(user_message)

        # Merge new info into memory
        self.merge_with_memory(extracted)

        # Check missing fields
        missing = self.get_missing_fields()

        if missing:
            ask = (
                "I still need the following details to recommend a portfolio:\n\n"
                + "\n".join(f"- {FRIENDLY_FIELD_NAMES[m]}" for m in missing)
                + "\n\nCould you please provide them?"
            )
            return {
                "sentiment": sentiment_class,
                "risk_profile": None,
                "portfolio": None,
                "response": ask
            }

        # All fields present → Predict risk
        risk_profile = predict_risk_profile(self.memory)

        # Build portfolio
        portfolio = build_portfolio_for_user(
            risk_profile,
            tickers=self.memory["tickers"]
        )

        # Friendly summary
        summary_prompt = f"""
        Summarize this portfolio:

        Sentiment: {sentiment_class}
        Risk Profile: {risk_profile}

        User Info:
        Age: {self.memory['age']}
        Income: {self.memory['income']}
        Risk Tolerance: {self.memory['tolerance']}
        Horizon: {self.memory['horizon_years']} years

        Tickers Used: {portfolio.get('tickers_used')}
        Weights: {portfolio.get('weights')}
        """

        summary = co.chat(model=self.MODEL, message=summary_prompt, temperature=0.4)

        return {
            "sentiment": sentiment_class,
            "risk_profile": risk_profile,
            "portfolio": portfolio,
            "response": summary.text.strip()
        }

chatbot_instance = Chatbot()
