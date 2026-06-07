from ta.trend import MACD
import pandas as pd


def calculate_macd(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate MACD indicator

    Returns:
        DataFrame with:
        - macd
        - signal
        - histogram
    """
    macd = MACD(close=data["close"])

    return pd.DataFrame({
        "macd": macd.macd(),
        "signal": macd.macd_signal(),
        "histogram": macd.macd_diff()
    })