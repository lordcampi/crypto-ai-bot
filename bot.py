import requests
import pandas as pd
import numpy as np

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD

from sklearn.ensemble import RandomForestClassifier

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from config import *

SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "DOGEUSDT"
]

# ==========================================
# BINANCE DATA
# ==========================================

def get_data(symbol):

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": "1h",
        "limit": 500
    }

    data = requests.get(
        url,
        params=params
    ).json()

    df = pd.DataFrame(data)

    df = df.iloc[:, :6]

    df.columns = [
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    for col in [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]:
        df[col] = df[col].astype(float)

    return df

# ==========================================
# INDICATORS
# ==========================================

def add_indicators(df):

    df["rsi"] = RSIIndicator(
        df["close"]
    ).rsi()

    df["ema20"] = EMAIndicator(
        df["close"],
        window=20
    ).ema_indicator()

    df["ema50"] = EMAIndicator(
        df["close"],
        window=50
    ).ema_indicator()

    macd = MACD(df["close"])

    df["macd"] = macd.macd()

    df["macd_signal"] = macd.macd_signal()

    df["return"] = df["close"].pct_change()

    df["target"] = np.where(
        df["close"].shift(-1)
        >
        df["close"],
        1,
        0
    )

    df.dropna(inplace=True)

    return df

# ==========================================
# MACHINE LEARNING
# ==========================================

def train_model(df):

    features = [
        "rsi",
        "ema20",
        "ema50",
        "macd",
        "macd_signal",
        "return"
    ]

    X = df[features]

    y = df["target"]

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X, y)

    return model

# ==========================================
# NEWS SENTIMENT
# ==========================================

def news_sentiment(symbol):

    analyzer = SentimentIntensityAnalyzer()

    coin = symbol.replace(
        "USDT",
        ""
    )

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={coin}&apiKey={NEWS_API_KEY}"
    )

    try:

        response = requests.get(url)

        articles = response.json()[
            "articles"
        ][:10]

        scores = []

        for article in articles:

            title = article["title"]

            sentiment = analyzer.polarity_scores(
                title
            )

            scores.append(
                sentiment["compound"]
            )

        return np.mean(scores)

    except:

        return 0

# ==========================================
# RISK MANAGEMENT
# ==========================================

def calculate_risk(price):

    stop_loss = round(
        price * 0.98,
        2
    )

    take_profit = round(
        price * 1.04,
        2
    )

    risk_amount = (
        CAPITAL * RISK_PER_TRADE
    )

    position_size = round(
        risk_amount /
        (price - stop_loss),
        4
    )

    return {
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "position_size": position_size
    }

# ==========================================
# MAIN ANALYSIS
# ==========================================

def analyze():

    results = []

    for symbol in SYMBOLS:

        df = get_data(symbol)

        df = add_indicators(df)

        model = train_model(df)

        latest = df.iloc[-1:]

        features = [
            "rsi",
            "ema20",
            "ema50",
            "macd",
            "macd_signal",
            "return"
        ]

        probability = model.predict_proba(
            latest[features]
        )[0][1]

        sentiment = news_sentiment(symbol)

        volume_score = (
            latest["volume"].values[0]
            /
            df["volume"].mean()
        )

        score = (
            probability * 0.5
            +
            ((sentiment + 1) / 2) * 0.2
            +
            min(volume_score / 2, 1) * 0.3
        )

        price = latest[
            "close"
        ].values[0]

        risk = calculate_risk(price)

        results.append({

            "symbol": symbol,
            "score": round(score, 3),
            "probability": round(
                probability * 100,
                2
            ),
            "sentiment": round(
                sentiment,
                2
            ),
            "price": round(price, 2),
            "stop_loss":
                risk["stop_loss"],
            "take_profit":
                risk["take_profit"],
            "position_size":
                risk["position_size"]
        })

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results