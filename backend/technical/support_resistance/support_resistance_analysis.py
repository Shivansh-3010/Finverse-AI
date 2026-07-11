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

ZONE_PERCENT = 0.02

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
    
    support_strength = None
    resistance_strength = None

    for level in scored_levels:

        if (
            level.level_type == "support"
            and level.level == nearest_support
        ):
            support_strength = level.strength

        if (
            level.level_type == "resistance"
            and level.level == nearest_resistance
        ):
            resistance_strength = level.strength
    
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
                
    distance_to_support_pct = None
    distance_to_resistance_pct = None

    if nearest_support is not None:

        distance_to_support_pct = (
            (current_price - nearest_support)
            / current_price
        ) * 100

    if nearest_resistance is not None:

        distance_to_resistance_pct = (
            (nearest_resistance - current_price)
            / current_price
        ) * 100


    breakout_zone_lower = None
    breakout_zone_upper = None

    if nearest_resistance is not None:

        breakout_zone_upper = nearest_resistance

        breakout_zone_lower = (
            nearest_resistance * (1 - ZONE_PERCENT)
        )


    breakdown_zone_lower = None
    breakdown_zone_upper = None

    if nearest_support is not None:

        breakdown_zone_lower = nearest_support

        breakdown_zone_upper = (
            nearest_support * (1 + ZONE_PERCENT)
        )
        
    distance_to_support_pct = (
        round(
            distance_to_support_pct,
            4
        )
        if distance_to_support_pct is not None
        else None
    )

    distance_to_resistance_pct = (
        round(
            distance_to_resistance_pct,
            4
        )
        if distance_to_resistance_pct is not None
        else None
    )

    breakout_zone_lower = (
        round(
            breakout_zone_lower,
            4
        )
        if breakout_zone_lower is not None
        else None
    )

    breakout_zone_upper = (
        round(
            breakout_zone_upper,
            4
        )
        if breakout_zone_upper is not None
        else None
    )

    breakdown_zone_lower = (
        round(
            breakdown_zone_lower,
            4
        )
        if breakdown_zone_lower is not None
        else None
    )

    breakdown_zone_upper = (
        round(
            breakdown_zone_upper,
            4
        )
        if breakdown_zone_upper is not None
        else None
    )

    return SupportResistanceAnalysis(
        supports=supports,
        resistances=resistances,

        nearest_support=nearest_support,
        nearest_resistance=nearest_resistance,

        support_strength=support_strength,
        resistance_strength=resistance_strength,

        distance_to_support_pct=distance_to_support_pct,
        distance_to_resistance_pct=distance_to_resistance_pct,

        breakout_zone_lower=breakout_zone_lower,
        breakout_zone_upper=breakout_zone_upper,

        breakdown_zone_lower=breakdown_zone_lower,
        breakdown_zone_upper=breakdown_zone_upper,

        signal=signal,
        signal_level=signal_level,
    )