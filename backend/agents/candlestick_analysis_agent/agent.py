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

        return analyze_candlestick(
            records
        )