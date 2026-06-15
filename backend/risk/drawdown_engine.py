import pandas as pd


class DrawdownEngine:
    """
    Calculates maximum drawdown and risk classification.
    """

    @staticmethod
    def calculate_drawdown(close_prices: pd.Series) -> pd.Series:
        running_max = close_prices.cummax()
        drawdown = (close_prices - running_max) / running_max
        return drawdown

    @classmethod
    def max_drawdown(cls, close_prices: pd.Series) -> float:
        drawdown = cls.calculate_drawdown(close_prices)
        return float(drawdown.min() * 100)

    @staticmethod
    def classify_drawdown(drawdown_percent: float) -> str:
        drawdown_percent = abs(drawdown_percent)

        if drawdown_percent < 10:
            return "Low"

        if drawdown_percent < 20:
            return "Moderate"

        if drawdown_percent < 35:
            return "High"

        return "Very High"