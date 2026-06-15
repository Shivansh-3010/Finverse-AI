import pandas as pd


class ExpectedShortfallEngine:
    """
    Conditional Value-at-Risk (CVaR)
    Also known as Expected Shortfall.
    """

    @staticmethod
    def calculate_expected_shortfall(
        close_prices: pd.Series,
        confidence_level: float = 0.95
    ) -> float:

        returns = close_prices.pct_change().dropna()

        threshold = returns.quantile(
            1 - confidence_level
        )

        tail_losses = returns[
            returns <= threshold
        ]

        if tail_losses.empty:
            return 0.0

        return float(abs(tail_losses.mean()) * 100)