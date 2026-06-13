class NewsScoreInterpreter:

    @staticmethod
    def interpret(
        score: int
    ):

        if score <= 20:
            return "very_negative"

        if score <= 40:
            return "negative"

        if score <= 60:
            return "neutral"

        if score <= 80:
            return "positive"

        return "very_positive"