from ta.volume import MFIIndicator
import pandas as pd


def calculate_mfi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Money Flow Index (MFI)

    Range: 0-100

    <20  -> Oversold
    >80  -> Overbought
    """

    mfi = MFIIndicator(
        high=data["high"],
        low=data["low"],
        close=data["close"],
        volume=data["volume"],
        window=period,
    )

    return mfi.money_flow_index()