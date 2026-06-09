from .pattern_detector import (
    detect_doji,
    detect_hammer,
    detect_shooting_star,
    detect_spinning_top,
    detect_bullish_engulfing,
    detect_bearish_engulfing,
    detect_morning_star,
    detect_evening_star,
    detect_three_white_soldiers,
    detect_three_black_crows,
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
        
    if detect_spinning_top(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Spinning Top",
            "signal": PatternSignal.NEUTRAL,
            "strength": 5,
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
            
    if len(records) >= 3:

        third = records[0]
        second = records[1]
        first = records[2]

        if detect_morning_star(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Morning Star",
                "signal": PatternSignal.BULLISH,
                "strength": 15,
            })
            
        if detect_evening_star(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Evening Star",
                "signal": PatternSignal.BEARISH,
                "strength": 15,
            })

        if detect_three_white_soldiers(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Three White Soldiers",
                "signal": PatternSignal.BULLISH,
                "strength": 15,
            })

        if detect_three_black_crows(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Three Black Crows",
                "signal": PatternSignal.BEARISH,
                "strength": 15,
            })
        
    score = calculate_pattern_score(patterns)

    return {
        "candlestick_score": score,
        "patterns": patterns,
    }