from ta.volume import VolumeWeightedAveragePrice
import pandas as pd


def calculate_vwap(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate VWAP (Volume Weighted Average Price)

    Args:
        data: OHLCV DataFrame
        period: VWAP period

    Returns:
        VWAP series
    """
    vwap = VolumeWeightedAveragePrice(
        high=data["high"],
        low=data["low"],
        close=data["close"],
        volume=data["volume"],
        window=period,
    )

    return vwap.volume_weighted_average_price()