from typing import List

from technical.support_resistance.models import (
    ClusteredLevel,
    LevelStrength,
)


def calculate_level_strength(
    levels: List[ClusteredLevel]
) -> List[LevelStrength]:
    """
    Convert clustered levels into strength scores.

    Current scoring:
    - More touches = stronger level

    Score capped at 100.
    """

    results = []

    for level in levels:

        strength = min(
            level.touches * 20,
            100
        )

        results.append(
            LevelStrength(
                level=level.level,
                level_type=level.level_type,
                touches=level.touches,
                strength=float(strength)
            )
        )

    return results