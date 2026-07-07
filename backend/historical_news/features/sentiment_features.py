import pandas as pd


class SentimentFeatureBuilder:

    SENTIMENT_MAP = {
        "positive": 1,
        "neutral": 0,
        "negative": -1,
    }

    @classmethod
    def build(
        cls,
        group: pd.DataFrame,
    ):

        news_count = len(group)

        positive_count = (
            group["sentiment"]
            .eq("positive")
            .sum()
        )

        negative_count = (
            group["sentiment"]
            .eq("negative")
            .sum()
        )

        neutral_count = (
            group["sentiment"]
            .eq("neutral")
            .sum()
        )

        positive_ratio = (
            positive_count / news_count
            if news_count
            else 0.0
        )

        negative_ratio = (
            negative_count / news_count
            if news_count
            else 0.0
        )

        avg_confidence = float(
            group["confidence"].mean()
        )

        sentiment_score = float(
            group["sentiment"]
            .map(cls.SENTIMENT_MAP)
            .mean()
        )

        return {
            "news_count": news_count,
            "positive_count": int(
                positive_count
            ),
            "negative_count": int(
                negative_count
            ),
            "neutral_count": int(
                neutral_count
            ),
            "positive_ratio": positive_ratio,
            "negative_ratio": negative_ratio,
            "avg_confidence": avg_confidence,
            "sentiment_score": sentiment_score,
        }