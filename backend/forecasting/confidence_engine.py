class ConfidenceEngine:

    @staticmethod
    def calculate(
        mae: float,
        directional_accuracy: float,
    ) -> float:

        mae_score = max(
            0,
            100 - (mae * 20)
        )

        confidence = (
            mae_score * 0.4
            +
            directional_accuracy * 0.6
        )

        return round(
            min(
                confidence,
                100
            ),
            2
        )