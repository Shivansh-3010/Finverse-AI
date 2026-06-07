from technical.trend.ema import calculate_ema
from technical.momentum.rsi import calculate_rsi
from technical.scoring.technical_score import calculate_technical_score


class TechnicalAnalysisAgent:
    """
    Phase 7 MVP Technical Analysis Agent
    """

    def analyze(self, data):
        rsi_series = calculate_rsi(data)
        ema_series = calculate_ema(data)

        latest_rsi = float(rsi_series.iloc[-1])

        latest_close = float(data["close"].iloc[-1])
        latest_ema = float(ema_series.iloc[-1])

        ema_bullish = latest_close > latest_ema

        result = calculate_technical_score(
            rsi=latest_rsi,
            macd_bullish=False,  # MACD integration later
            ema_bullish=ema_bullish,
        )

        return {
            "trend": "bullish" if ema_bullish else "bearish",
            "rsi": round(latest_rsi, 2),
            "technical_score": result["technical_score"],
            "reasons": result["reasons"],
        }