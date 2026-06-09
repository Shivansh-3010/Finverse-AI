from .pattern_detector import (
    detect_doji,
    detect_hammer,
    detect_shooting_star,
    detect_bullish_engulfing,
    detect_bearish_engulfing,
)

from .pattern_scoring import (
    calculate_pattern_score,
)

from .pattern_types import PatternSignal


def analyze_candlestick(records):
    
    latest = records[0]

    open_price = float(latest.open)
    high_price = float(latest.high)
    low_price = float(latest.low)
    close_price = float(latest.close)
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
    
    if len(records) >= 2:

        previous = records[1]

        if detect_bullish_engulfing(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bullish Engulfing",
                "signal": PatternSignal.BULLISH,
                "strength": 10,
            })

        if detect_bearish_engulfing(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bearish Engulfing",
                "signal": PatternSignal.BEARISH,
                "strength": 10,
            })
            
        score = calculate_pattern_score(patterns)

    return {
        "candlestick_score": score,
        "patterns": patterns,
    }