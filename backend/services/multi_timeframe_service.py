from schemas.multi_timeframe_analysis import (
    MultiTimeframeAnalysisResponse,
    TimeframeSignal,
)
from constants.timeframes import (
    SUPPORTED_TIMEFRAMES,
)

from services.technical_analysis_service import (
    TechnicalAnalysisService,
)


class MultiTimeframeService:
    
    TIMEFRAME_WEIGHTS = {
        "1m": 1,
        "5m": 2,
        "15m": 3,
        "1h": 4,
        "4h": 5,
        "1d": 6,
        "1w": 8,
        "1mo": 10,
    }
    
    @staticmethod
    def score_to_trend(
        score: float
    ):

        if score >= 60:
            return "bullish"

        if score <= 40:
            return "bearish"

        return "neutral"

    @staticmethod
    def analyze(
        symbol: str
    ) -> MultiTimeframeAnalysisResponse:

        signals = []

        bullish_score = 0
        bearish_score = 0
        neutral_score = 0

        for timeframe in SUPPORTED_TIMEFRAMES:

            try:

                result = (
                    TechnicalAnalysisService.analyze(
                        symbol=symbol,
                        timeframe=timeframe
                    )
                )

                score = result.get(
                    "combined_score",
                    result.get(
                        "technical_score",
                        50
                    )
                )

                trend = (
                    MultiTimeframeService
                    .score_to_trend(score)
                )

                weight = (
                    MultiTimeframeService
                    .TIMEFRAME_WEIGHTS[timeframe]
                )

                if trend == "bullish":
                    bullish_score += weight

                elif trend == "bearish":
                    bearish_score += weight

                else:
                    neutral_score += weight

                signals.append(
                    TimeframeSignal(
                        timeframe=timeframe,
                        trend=trend
                    )
                )

            except Exception:

                signals.append(
                    TimeframeSignal(
                        timeframe=timeframe,
                        trend="unknown"
                    )
                )

        if (
            bullish_score > bearish_score
            and bullish_score > neutral_score
        ):
            overall_trend = "bullish"

        elif (
            bearish_score > bullish_score
            and bearish_score > neutral_score
        ):
            overall_trend = "bearish"

        else:
            overall_trend = "neutral"

        return MultiTimeframeAnalysisResponse(
            overall_trend=overall_trend,
            signals=signals
        )