from ta.volatility import AverageTrueRange
import pandas as pd


def calculate_atr(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Average True Range (ATR)

    Args:
        data: OHLCV DataFrame
        period: ATR period

    Returns:
        ATR series
    """
    atr = AverageTrueRange(
        high=data["high"],
        low=data["low"],
        close=data["close"],
        window=period,
    )

    return atr.average_true_range()