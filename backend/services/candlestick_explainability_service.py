from schemas.candlestick_explanation import (
    CandlestickExplanation,
)


class CandlestickExplainabilityService:

    EXPLANATIONS = {
        "Doji": (
            "Neutral",
            "Market indecision between buyers and sellers."
        ),

        "Hammer": (
            "Bullish",
            "Buyers rejected lower prices and pushed the candle higher."
        ),

        "Shooting Star": (
            "Bearish",
            "Sellers rejected higher prices after a bullish move."
        ),

        "Spinning Top": (
            "Neutral",
            "Neither buyers nor sellers gained clear control."
        ),

        "Bullish Engulfing": (
            "Bullish",
            "Buyers completely overwhelmed the previous bearish candle."
        ),

        "Bearish Engulfing": (
            "Bearish",
            "Sellers completely overwhelmed the previous bullish candle."
        ),

        "Morning Star": (
            "Bullish",
            "A potential reversal showing buyers taking control."
        ),

        "Evening Star": (
            "Bearish",
            "A potential reversal showing sellers taking control."
        ),

        "Three White Soldiers": (
            "Bullish",
            "Strong sustained buying pressure over three candles."
        ),

        "Three Black Crows": (
            "Bearish",
            "Strong sustained selling pressure over three candles."
        ),
    }

    @staticmethod
    def explain(
        pattern: str
    ) -> CandlestickExplanation:

        signal, reason = (
            CandlestickExplainabilityService
            .EXPLANATIONS.get(
                pattern,
                (
                    "Neutral",
                    "No explanation available."
                ),
            )
        )

        return CandlestickExplanation(
            pattern=pattern,
            signal=signal,
            reason=reason,
        )