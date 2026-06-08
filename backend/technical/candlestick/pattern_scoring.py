from .pattern_types import PatternSignal


def calculate_pattern_score(patterns: list[dict]) -> float:
    """
    Calculate normalized candlestick score (0-100)
    """

    score = 50

    for pattern in patterns:
        signal = pattern["signal"]
        strength = pattern["strength"]

        if signal == PatternSignal.BULLISH:
            score += strength

        elif signal == PatternSignal.BEARISH:
            score -= strength

    score = max(0, min(100, score))

    return round(score, 2)