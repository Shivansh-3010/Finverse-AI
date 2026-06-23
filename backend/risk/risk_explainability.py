class RiskExplainability:

    @staticmethod
    def explain(
        volatility: float,
        drawdown: float,
        risk_score: int,
        var_95: float = 0.0,
        expected_shortfall: float = 0.0,
    ) -> str:

        reasons = []

        if volatility > 50:
            reasons.append(
                "extreme volatility detected"
            )

        elif volatility > 30:
            reasons.append(
                "high volatility detected"
            )

        if abs(drawdown) > 40:
            reasons.append(
                "severe historical drawdown"
            )

        elif abs(drawdown) > 20:
            reasons.append(
                "elevated drawdown detected"
            )

        if var_95 > 5:
            reasons.append(
                "high downside tail risk"
            )

        if expected_shortfall > 7:
            reasons.append(
                "large expected losses during stress periods"
            )

        if risk_score >= 80:
            reasons.append(
                "overall risk profile is very high"
            )

        if not reasons:
            reasons.append(
                "stable risk profile"
            )

        return ", ".join(reasons)