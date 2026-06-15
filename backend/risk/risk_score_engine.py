class RiskScoreEngine:
    """
    Converts multiple risk metrics
    into a normalized 0-100 risk score.
    """

    @staticmethod
    def calculate_score(
        volatility: float,
        drawdown: float,
        var_95: float,
        expected_shortfall: float
    ) -> int:

        volatility_score = min(volatility * 2, 100)

        drawdown_score = min(
            abs(drawdown) * 2.5,
            100
        )

        var_score = min(
            var_95 * 10,
            100
        )

        es_score = min(
            expected_shortfall * 10,
            100
        )

        score = (
            volatility_score * 0.30 +
            drawdown_score * 0.30 +
            var_score * 0.20 +
            es_score * 0.20
        )

        return int(round(score))

    @staticmethod
    def classify_risk(score: int) -> str:

        if score <= 20:
            return "Very Low Risk"

        if score <= 40:
            return "Low Risk"

        if score <= 60:
            return "Moderate Risk"

        if score <= 80:
            return "High Risk"

        return "Very High Risk"