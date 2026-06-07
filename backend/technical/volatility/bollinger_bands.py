from ta.volatility import BollingerBands
import pandas as pd


def calculate_bollinger_bands(
    data: pd.DataFrame,
    period: int = 20,
    std_dev: int = 2
) -> pd.DataFrame:
    """
    Calculate Bollinger Bands

    Returns:
        DataFrame with:
        - upper_band
        - middle_band
        - lower_band
    """
    bb = BollingerBands(
        close=data["close"],
        window=period,
        window_dev=std_dev
    )

    return pd.DataFrame({
        "upper_band": bb.bollinger_hband(),
        "middle_band": bb.bollinger_mavg(),
        "lower_band": bb.bollinger_lband(),
    })