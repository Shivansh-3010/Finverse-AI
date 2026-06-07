import pandas as pd


def calculate_ema(data: pd.DataFrame, period: int = 20) -> pd.Series:
    """
    Calculate Exponential Moving Average (EMA)

    Args:
        data: DataFrame containing OHLCV data
        period: EMA period

    Returns:
        EMA series
    """
    return data["close"].ewm(span=period, adjust=False).mean()