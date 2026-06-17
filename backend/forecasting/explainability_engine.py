class ExplainabilityEngine:

    @staticmethod
    def explain(
        direction: str,
        confidence: float,
        xgb_return: float,
        prophet_return: float,
    ):

        reasons = []

        if xgb_return > 0:
            reasons.append(
                "XGBoost forecasts positive returns"
            )
        else:
            reasons.append(
                "XGBoost forecasts negative returns"
            )

        if prophet_return > 0:
            reasons.append(
                "Prophet forecasts upward price movement"
            )
        else:
            reasons.append(
                "Prophet forecasts downward price movement"
            )

        if confidence >= 80:
            confidence_label = (
                "high confidence"
            )
        elif confidence >= 60:
            confidence_label = (
                "moderate confidence"
            )
        else:
            confidence_label = (
                "low confidence"
            )

        return {
            "forecast": (
                "BUY"
                if direction == "bullish"
                else "SELL"
            ),
            "confidence": confidence,
            "reason":
                ", ".join(reasons)
                + f" with {confidence_label}.",
        }