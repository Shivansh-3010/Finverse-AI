from ta.volume import OnBalanceVolumeIndicator
import pandas as pd


def calculate_obv(data: pd.DataFrame) -> pd.Series:
    """
    Calculate On-Balance Volume (OBV)

    Args:
        data: OHLCV DataFrame

    Returns:
        OBV series
    """
    obv = OnBalanceVolumeIndicator(
        close=data["close"],
        volume=data["volume"]
    )

    return obv.on_balance_volume()