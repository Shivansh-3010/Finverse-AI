from .pattern_reliability import (
    get_pattern_reliability,
)


def calculate_pattern_confidence(
    pattern_name: str,
    strength: int,
) -> float:
    """
    Calculate pattern confidence using:

    1. Historical reliability
    2. Pattern strength
    """

    reliability = (
        get_pattern_reliability(
            pattern_name
        )
    )

    confidence = (
        reliability
        + (strength * 0.5)
    )

    return round(
        min(confidence, 95),
        2
    )