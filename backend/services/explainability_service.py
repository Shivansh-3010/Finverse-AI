from schemas.indicator_explanation import IndicatorExplanation


class ExplainabilityService:

    @staticmethod
    def explain_rsi(rsi: float) -> IndicatorExplanation:

        if rsi < 30:
            return IndicatorExplanation(
                indicator="RSI",
                value=rsi,
                signal="Bullish",
                reason="Oversold condition detected"
            )

        if rsi > 70:
            return IndicatorExplanation(
                indicator="RSI",
                value=rsi,
                signal="Bearish",
                reason="Overbought condition detected"
            )

        return IndicatorExplanation(
            indicator="RSI",
            value=rsi,
            signal="Neutral",
            reason="RSI is within normal range"
        )