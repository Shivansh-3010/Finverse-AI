from forecasting.prediction_engine import (
    PredictionEngine,
)


def test():

    engine = (
        PredictionEngine()
    )

    prediction = (
        engine.predict(
            {
                "rsi": 50,
                "macd": 0,
                "macd_signal": 0,
                "atr": 20,
                "adx": 25,
                "mfi": 50,
                "obv": 1000000,
                "vwap": 1300,
                "bb_upper": 1400,
                "bb_middle": 1350,
                "bb_lower": 1300,
                "strength": 10,
                "confidence": 80,
                "candlestick_score": 60,
                "avg_news_score": 0,
                "avg_news_confidence": 0,
                "article_count": 0,
                "recent_article_count": 0,
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0,
            }
        )
    )

    print(
        "Prediction:",
        prediction
    )


if __name__ == "__main__":
    test()