class SentimentEngine:

    POSITIVE = "positive"

    NEUTRAL = "neutral"

    NEGATIVE = "negative"

    @staticmethod
    def build_response(
        sentiment: str,
        confidence: float
    ):

        return {
            "sentiment": sentiment,
            "confidence": confidence
        }