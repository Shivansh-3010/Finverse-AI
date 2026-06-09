def calculate_pattern_confidence(
    pattern_name: str,
    strength: int,
) -> int:
    """
    Pattern confidence score (0-100).

    Phase 8 MVP confidence framework.
    """

    confidence_map = {
        "Doji": 65,
        "Spinning Top": 65,

        "Hammer": 80,
        "Shooting Star": 80,

        "Bullish Engulfing": 85,
        "Bearish Engulfing": 85,

        "Morning Star": 92,
        "Evening Star": 92,

        "Three White Soldiers": 95,
        "Three Black Crows": 95,
    }

    return confidence_map.get(
        pattern_name,
        min(
            95,
            max(
                60,
                strength * 6,
            ),
        ),
    )