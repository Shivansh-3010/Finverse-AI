from services.candlestick_analysis_service import (
    CandlestickAnalysisService,
)
from constants.timeframes import (
    SUPPORTED_TIMEFRAMES,
)
from constants.pattern_timeframe_weights import (
    TIMEFRAME_WEIGHTS,
)


class MultiTimeframePatternService:

    @staticmethod
    def analyze(
        symbol: str,
    ):

        results = []

        for timeframe in SUPPORTED_TIMEFRAMES:

            results.append(
                {
                    "timeframe": timeframe,
                    "patterns": (
                        CandlestickAnalysisService.analyze(
                            symbol=symbol,
                            timeframe=timeframe,
                        )["patterns"]
                    ),
                }
            )
            
        bullish_score = 0
        bearish_score = 0

        for item in results:
            
            weight = TIMEFRAME_WEIGHTS.get(
                item["timeframe"],
                1
            )

            for pattern in item["patterns"]:
                
                pattern_score = (
                    weight
                    * pattern["strength"]
                    * (
                        pattern["confidence"]
                        / 100
                    )
                )

                signal = pattern["signal"]

                if signal.value == "Bullish":
                    bullish_score += pattern_score

                elif signal.value == "Bearish":
                    bearish_score += pattern_score

        ratio = (
            bullish_score
            / max(bearish_score, 1)
        )

        if ratio >= 1.5:

            overall_alignment = "strong_bullish"

        elif ratio > 1.0:

            overall_alignment = "bullish"

        elif ratio <= 0.67:

            overall_alignment = "strong_bearish"

        elif ratio < 1.0:

            overall_alignment = "bearish"

        else:

            overall_alignment = "neutral"
            
        alignment_confidence = round(
            (
                max(
                    bullish_score,
                    bearish_score,
                )
                /
                max(
                    bullish_score + bearish_score,
                    1,
                )
            ) * 100,
            2,
        )

        return {
            "symbol": symbol,
            "overall_alignment": overall_alignment,
            "alignment_confidence": alignment_confidence,
            "bullish_score": round(
                bullish_score,
                2,
            ),
            "bearish_score": round(
                bearish_score,
                2,
            ),
            "timeframes": results,
        }