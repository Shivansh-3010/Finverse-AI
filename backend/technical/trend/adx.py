from ta.trend import ADXIndicator
import pandas as pd


def calculate_adx(data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Calculate ADX, DI+ and DI-
    """

    adx = ADXIndicator(
        high=data["high"],
        low=data["low"],
        close=data["close"],
        window=period
    )

    return pd.DataFrame({
        "adx": adx.adx(),
        "di_plus": adx.adx_pos(),
        "di_minus": adx.adx_neg(),
    })