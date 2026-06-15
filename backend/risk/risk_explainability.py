class RiskExplainability:

    @staticmethod
    def explain(
        volatility: float,
        drawdown: float,
        risk_score: int
    ) -> str:

        reasons = []

        if volatility > 30:
            reasons.append(
                "high volatility detected"
            )

        if abs(drawdown) > 20:
            reasons.append(
                "elevated drawdown detected"
            )

        if not reasons:
            reasons.append(
                "stable risk profile"
            )

        return ", ".join(reasons)