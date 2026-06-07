import pandas as pd


def calculate_sma(data: pd.DataFrame, period: int = 20) -> pd.Series:
    """
    Calculate Simple Moving Average (SMA)

    Args:
        data: DataFrame containing OHLCV data
        period: SMA period

    Returns:
        SMA series
    """
    return data["close"].rolling(window=period).mean()