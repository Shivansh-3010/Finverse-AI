from .pattern_types import PatternSignal


def adjust_pattern_strength(
    signal,
    strength,
    trend,
):

    if signal == PatternSignal.BULLISH:

        if trend == "downtrend":
            return strength + 3

        if trend == "uptrend":
            return max(
                strength - 2,
                1
            )

    if signal == PatternSignal.BEARISH:

        if trend == "uptrend":
            return strength + 3

        if trend == "downtrend":
            return max(
                strength - 2,
                1
            )

    return strength