from technical.candlestick.candlestick_analysis import (
    analyze_candlestick,
)


class CandlestickAnalysisAgent:
    """
    Phase 8 MVP Candlestick Analysis Agent
    """

    def analyze(
        self,
        records,
    ):
        latest = records[0]

        return analyze_candlestick(
            open_price=float(latest.open),
            high_price=float(latest.high),
            low_price=float(latest.low),
            close_price=float(latest.close),
        )