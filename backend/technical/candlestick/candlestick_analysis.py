from .pattern_detector import (
    detect_doji,
    detect_hammer,
    detect_shooting_star,
)

from .pattern_scoring import (
    calculate_pattern_score,
)

from .pattern_types import PatternSignal


def analyze_candlestick(
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
        
    if detect_shooting_star(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Shooting Star",
            "signal": PatternSignal.BEARISH,
            "strength": 8,
        })

    score = calculate_pattern_score(patterns)

    return {
        "candlestick_score": score,
        "patterns": patterns,
    }