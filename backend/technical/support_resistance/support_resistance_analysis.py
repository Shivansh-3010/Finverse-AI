from typing import Optional

import pandas as pd

from technical.support_resistance.pivot_detection import (
    detect_pivots,
)
from technical.support_resistance.level_clustering import (
    cluster_levels,
)
from technical.support_resistance.level_strength import (
    calculate_level_strength,
)
from technical.support_resistance.models import (
    SupportResistanceAnalysis,
)


def analyze_support_resistance(
    df: pd.DataFrame,
    current_price: Optional[float] = None,
):
    """
    Full Support & Resistance pipeline.

    Steps:
    1. Detect pivots
    2. Cluster levels
    3. Score levels
    4. Find nearest support/resistance
    """

    if df.empty:
        return SupportResistanceAnalysis(
            supports=[],
            resistances=[],
            nearest_support=None,
            nearest_resistance=None,
        )

    pivots = detect_pivots(
        df,
        window=5
    )

    clustered_levels = cluster_levels(pivots)

    scored_levels = calculate_level_strength(
        clustered_levels
    )

    if current_price is None:
        current_price = float(
            df["close"].iloc[-1]
        )
        
    previous_close = None

    if len(df) >= 2:
        previous_close = float(
            df["close"].iloc[-2]
        )

    supports = sorted(
        [
            level.level
            for level in scored_levels
            if level.level_type == "support"
        ],
        reverse=True,
    )

    resistances = sorted(
        [
            level.level
            for level in scored_levels
            if level.level_type == "resistance"
        ]
    )

    nearest_support = next(
        (
            level
            for level in supports
            if level < current_price
        ),
        None,
    )

    nearest_resistance = next(
        (
            level
            for level in resistances
            if level > current_price
        ),
        None,
    )
    
    signal = None
    signal_level = None

    if previous_close is not None:

        for resistance in resistances:

            if (
                previous_close <= resistance
                and current_price > resistance
            ):
                signal = "breakout"
                signal_level = resistance
                break

        if signal is None:

            for support in supports:

                if (
                    previous_close >= support
                    and current_price < support
                ):
                    signal = "breakdown"
                    signal_level = support
                    break

    return SupportResistanceAnalysis(
        supports=supports,
        resistances=resistances,
        nearest_support=nearest_support,
        nearest_resistance=nearest_resistance,
        signal=signal,
        signal_level=signal_level,
    )