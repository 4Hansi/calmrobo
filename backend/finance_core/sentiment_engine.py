# backend/finance_core/sentiment_engine.py
import nltk
from textblob import TextBlob
from typing import Text, Dict

# Ensure necessary NLTK data is present (first run will download; it's fast)
try:
    nltk.data.find('corpora/wordnet')
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('wordnet', quiet=True)
    nltk.download('punkt', quiet=True)

def get_sentiment(text: Text) -> Dict[Text, float]:
    """
    Returns polarity (-1..1) and subjectivity (0..1)
    """
    if not text:
        return {"polarity": 0.0, "subjectivity": 0.0}
    analysis = TextBlob(text)
    return {
        "polarity": float(analysis.sentiment.polarity),
        "subjectivity": float(analysis.sentiment.subjectivity),
    }

def classify_sentiment(polarity: float) -> Text:
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"
