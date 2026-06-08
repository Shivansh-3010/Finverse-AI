from schemas.multi_timeframe_analysis import (
    MultiTimeframeAnalysisResponse,
    TimeframeSignal,
)


class MultiTimeframeService:

    @staticmethod
    def analyze(symbol: str) -> MultiTimeframeAnalysisResponse:
        """
        Temporary Phase 7 implementation.

        Later each timeframe will calculate
        real indicators from TimescaleDB.
        """

        signals = [
            TimeframeSignal(timeframe="15m", trend="bullish"),
            TimeframeSignal(timeframe="1h", trend="bullish"),
            TimeframeSignal(timeframe="4h", trend="neutral"),
            TimeframeSignal(timeframe="1D", trend="bullish"),
            TimeframeSignal(timeframe="1W", trend="bullish"),
        ]

        bullish_count = sum(
            1 for signal in signals
            if signal.trend == "bullish"
        )

        overall_trend = (
            "bullish"
            if bullish_count >= 3
            else "neutral"
        )

        return MultiTimeframeAnalysisResponse(
            overall_trend=overall_trend,
            signals=signals
        )