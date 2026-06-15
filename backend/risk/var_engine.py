import pandas as pd


class ValueAtRiskEngine:
    """
    Historical Value-at-Risk (VaR).
    """

    @staticmethod
    def calculate_var(
        close_prices: pd.Series,
        confidence_level: float = 0.95
    ) -> float:
        returns = close_prices.pct_change().dropna()

        percentile = (1 - confidence_level) * 100

        var = returns.quantile(percentile / 100)

        return float(abs(var) * 100)