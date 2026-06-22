from typing import List

import pandas as pd

from technical.support_resistance.models import PivotPoint


def detect_pivots(
    df: pd.DataFrame,
    window: int = 5
) -> List[PivotPoint]:
    """
    Detect swing highs and swing lows.

    Required columns:
    - high
    - low
    """

    pivots = []

    if len(df) < (window * 2 + 1):
        return pivots

    for i in range(window, len(df) - window):

        current_high = df["high"].iloc[i]
        current_low = df["low"].iloc[i]

        left_highs = df["high"].iloc[i - window:i]
        right_highs = df["high"].iloc[i + 1:i + window + 1]

        left_lows = df["low"].iloc[i - window:i]
        right_lows = df["low"].iloc[i + 1:i + window + 1]

        is_pivot_high = (
            current_high > left_highs.max()
            and current_high > right_highs.max()
        )

        is_pivot_low = (
            current_low < left_lows.min()
            and current_low < right_lows.min()
        )

        if is_pivot_high:
            pivots.append(
                PivotPoint(
                    index=i,
                    price=float(current_high),
                    pivot_type="high"
                )
            )

        if is_pivot_low:
            pivots.append(
                PivotPoint(
                    index=i,
                    price=float(current_low),
                    pivot_type="low"
                )
            )

    return pivots