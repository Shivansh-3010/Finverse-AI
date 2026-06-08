from technical.candlestick.pattern_detector import (
    detect_doji,
    detect_hammer,
)

from technical.candlestick.pattern_scoring import (
    calculate_pattern_score,
)

from technical.candlestick.pattern_types import (
    PatternSignal,
)


def generate_candlestick_features(
    open_price: float,
    high_price: float,
    low_price: float,
    close_price: float,
):
    patterns = []

    if detect_doji(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Doji",
            "signal": PatternSignal.NEUTRAL,
            "strength": 5,
        })

    if detect_hammer(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Hammer",
            "signal": PatternSignal.BULLISH,
            "strength": 8,
        })

    score = calculate_pattern_score(patterns)

    return {
        "patterns_detected": len(patterns),
        "pattern_score": score,
        "hammer_present": int(
            any(
                p["pattern"] == "Hammer"
                for p in patterns
            )
        ),
        "doji_present": int(
            any(
                p["pattern"] == "Doji"
                for p in patterns
            )
        ),
    }