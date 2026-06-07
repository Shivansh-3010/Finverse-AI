from ta.momentum import RSIIndicator
import pandas as pd


def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate RSI (Relative Strength Index)

    Args:
        data: DataFrame containing OHLCV data
        period: RSI period

    Returns:
        RSI series
    """
    rsi = RSIIndicator(close=data["close"], window=period)
    return rsi.rsi()