import numpy as np
import pandas as pd


class VolatilityEngine:
    """
    Calculates historical and annualized volatility.
    """

    TRADING_DAYS = 252

    @staticmethod
    def calculate_returns(close_prices: pd.Series) -> pd.Series:
        return close_prices.pct_change().dropna()

    @classmethod
    def historical_volatility(cls, close_prices: pd.Series) -> float:
        returns = cls.calculate_returns(close_prices)
        return float(returns.std())

    @classmethod
    def annualized_volatility(cls, close_prices: pd.Series) -> float:
        returns = cls.calculate_returns(close_prices)
        return float(returns.std() * np.sqrt(cls.TRADING_DAYS))

    @staticmethod
    def classify_volatility(volatility_percent: float) -> str:
        if volatility_percent < 15:
            return "Low"

        if volatility_percent < 30:
            return "Moderate"

        if volatility_percent < 50:
            return "High"

        return "Very High"