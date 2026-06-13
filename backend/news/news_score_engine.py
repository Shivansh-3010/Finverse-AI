class NewsScoreEngine:

    SENTIMENT_WEIGHTS = {

        "positive": 15,

        "neutral": 0,

        "negative": -15
    }

    @classmethod
    def calculate_score(
        cls,
        sentiment: str,
        confidence: float,
        event_score: int
    ):

        sentiment_score = (
            cls.SENTIMENT_WEIGHTS.get(
                sentiment,
                0
            )
        )

        confidence_bonus = int(
            confidence * 10
        )

        final_score = (
            50
            + sentiment_score
            + event_score
            + confidence_bonus
        )

        final_score = max(
            0,
            min(
                100,
                final_score
            )
        )

        return final_score