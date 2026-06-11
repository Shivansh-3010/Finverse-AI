from .pattern_detector import (
    detect_doji,
    detect_hammer,
    detect_shooting_star,
    detect_spinning_top,

    detect_inverted_hammer,
    detect_hanging_man,
    detect_dragonfly_doji,
    detect_gravestone_doji,
    detect_long_legged_doji,
    detect_marubozu,

    detect_bullish_engulfing,
    detect_bearish_engulfing,
    detect_bullish_harami,
    detect_bearish_harami,
    detect_piercing_line,
    detect_dark_cloud_cover,
    detect_tweezer_top,
    detect_tweezer_bottom,
    detect_harami_cross,
    detect_matching_high,
    detect_matching_low,
    detect_bullish_kicker,
    detect_bearish_kicker,

    detect_morning_star,
    detect_evening_star,
    detect_three_white_soldiers,
    detect_three_black_crows,
    detect_three_inside_up,
    detect_three_inside_down,
    detect_morning_doji_star,
    detect_evening_doji_star,
    detect_three_outside_up,
    detect_three_outside_down,
)

from .pattern_scoring import (
    calculate_pattern_score,
)
from .trend_context import (
    determine_trend,
)
from .trend_adjustment import (
    adjust_pattern_strength,
)
from .volume_confirmation import (
    calculate_volume_factor,
)
from .pattern_confidence import (
    calculate_pattern_confidence,
)

from .pattern_types import PatternSignal


def analyze_candlestick(records):
    
    closes = [
        float(record.close)
        for record in reversed(records)
    ]

    trend = determine_trend(
        closes
    )
    
    volume_factor = (
        calculate_volume_factor(
            records
        )
    )
    
    latest = records[0]

    open_price = float(latest.open)
    high_price = float(latest.high)
    low_price = float(latest.low)
    close_price = float(latest.close)
    patterns = []
    
    """ Single Candle Patterns"""

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
            "confidence": calculate_pattern_confidence(
                "Doji",
                5,
            ),
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
            "confidence": calculate_pattern_confidence(
                "Hammer",
                8,
            ),
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
            "confidence": calculate_pattern_confidence(
                "Shooting Star",
                8,
            ),
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
            "confidence": calculate_pattern_confidence(
                "Spinning Top",
                5,
            ),
        })
        
    if detect_inverted_hammer(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Inverted Hammer",
            "signal": PatternSignal.BULLISH,
            "strength": 8,
            "confidence": calculate_pattern_confidence(
                "Inverted Hammer",
                8,
            ),
        })

    if detect_hanging_man(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Hanging Man",
            "signal": PatternSignal.BEARISH,
            "strength": 8,
            "confidence": calculate_pattern_confidence(
                "Hanging Man",
                8,
            ),
        })

    if detect_dragonfly_doji(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Dragonfly Doji",
            "signal": PatternSignal.BULLISH,
            "strength": 6,
            "confidence": calculate_pattern_confidence(
                "Dragonfly Doji",
                6,
            ),
        })

    if detect_gravestone_doji(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Gravestone Doji",
            "signal": PatternSignal.BEARISH,
            "strength": 6,
            "confidence": calculate_pattern_confidence(
                "Gravestone Doji",
                6,
            ),
        })

    if detect_long_legged_doji(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Long-Legged Doji",
            "signal": PatternSignal.NEUTRAL,
            "strength": 5,
            "confidence": calculate_pattern_confidence(
                "Long-Legged Doji",
                5,
            ),
        })

    if detect_marubozu(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Marubozu",
            "signal": (
                PatternSignal.BULLISH
                if close_price > open_price
                else PatternSignal.BEARISH
            ),
            "strength": 10,
            "confidence": calculate_pattern_confidence(
                "Marubozu",
                10,
            ),
        })
        
    """ Double Candle Patterns """
    
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
                "confidence": calculate_pattern_confidence(
                    "Bullish Engulfing",
                    10,
                ),
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
                "confidence": calculate_pattern_confidence(
                    "Bearish Engulfing",
                    10,
                ),
            })
            
        if detect_bullish_harami(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bullish Harami",
                "signal": PatternSignal.BULLISH,
                "strength": 9,
                "confidence": calculate_pattern_confidence(
                    "Bullish Harami",
                    9,
                ),
            })

        if detect_bearish_harami(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bearish Harami",
                "signal": PatternSignal.BEARISH,
                "strength": 9,
                "confidence": calculate_pattern_confidence(
                    "Bearish Harami",
                    9,
                ),
            })

        if detect_piercing_line(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Piercing Line",
                "signal": PatternSignal.BULLISH,
                "strength": 10,
                "confidence": calculate_pattern_confidence(
                    "Piercing Line",
                    10,
                ),
            })

        if detect_dark_cloud_cover(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Dark Cloud Cover",
                "signal": PatternSignal.BEARISH,
                "strength": 10,
                "confidence": calculate_pattern_confidence(
                    "Dark Cloud Cover",
                    10,
                ),
            })
            
        if detect_tweezer_top(
            prev_high=float(previous.high),
            curr_high=high_price,
        ):
            patterns.append({
                "pattern": "Tweezer Top",
                "signal": PatternSignal.BEARISH,
                "strength": 8,
                "confidence": calculate_pattern_confidence(
                    "Tweezer Top",
                    8,
                ),
            })
            
        if detect_tweezer_bottom(
            prev_low=float(previous.low),
            curr_low=low_price,
        ):
            patterns.append({
                "pattern": "Tweezer Bottom",
                "signal": PatternSignal.BULLISH,
                "strength": 8,
                "confidence": calculate_pattern_confidence(
                    "Tweezer Bottom",
                    8,
                ),
            })
            
        if detect_harami_cross(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Harami Cross",
                "signal": PatternSignal.NEUTRAL,
                "strength": 7,
                "confidence": calculate_pattern_confidence(
                    "Harami Cross",
                    7,
                ),
            })
            
        if detect_matching_high(
            prev_close=float(previous.close),
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Matching High",
                "signal": PatternSignal.BEARISH,
                "strength": 7,
                "confidence": calculate_pattern_confidence(
                    "Matching High",
                    7,
                ),
            })
            
        if detect_matching_low(
            prev_low=float(previous.low),
            curr_low=low_price,
        ):
            patterns.append({
                "pattern": "Matching Low",
                "signal": PatternSignal.BULLISH,
                "strength": 7,
                "confidence": calculate_pattern_confidence(
                    "Matching Low",
                    7,
                ),
            })
            
        if detect_bullish_kicker(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bullish Kicker",
                "signal": PatternSignal.BULLISH,
                "strength": 12,
                "confidence": calculate_pattern_confidence(
                    "Bullish Kicker",
                    12,
                ),
            })
            
        if detect_bearish_kicker(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bearish Kicker",
                "signal": PatternSignal.BEARISH,
                "strength": 12,
                "confidence": calculate_pattern_confidence(
                    "Bearish Kicker",
                    12,
                ),
            })
            
    """ Triple Candle Patterns """
            
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
                "confidence": calculate_pattern_confidence(
                    "Morning Star",
                    15,
                ),
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
                "confidence": calculate_pattern_confidence(
                    "Evening Star",
                    15,
                ),
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
                "confidence": calculate_pattern_confidence(
                    "Three White Soldiers",
                    15,
                ),
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
                "confidence": calculate_pattern_confidence(
                    "Three Black Crows",
                    15,
                ),
            })
            
        if detect_three_inside_up(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Three Inside Up",
                "signal": PatternSignal.BULLISH,
                "strength": 12,
                "confidence": calculate_pattern_confidence(
                    "Three Inside Up",
                    12,
                ),
            })

        if detect_three_inside_down(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Three Inside Down",
                "signal": PatternSignal.BEARISH,
                "strength": 12,
                "confidence": calculate_pattern_confidence(
                    "Three Inside Down",
                    12,
                ),
            })
            
        if detect_morning_doji_star(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Morning Doji Star",
                "signal": PatternSignal.BULLISH,
                "strength": 15,
                "confidence": calculate_pattern_confidence(
                    "Morning Doji Star",
                    15,
                ),
            })
            
        if detect_evening_doji_star(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Evening Doji Star",
                "signal": PatternSignal.BEARISH,
                "strength": 15,
                "confidence": calculate_pattern_confidence(
                    "Evening Doji Star",
                    15,
                ),
            })
            
        if detect_three_outside_up(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Three Outside Up",
                "signal": PatternSignal.BULLISH,
                "strength": 14,
                "confidence": calculate_pattern_confidence(
                    "Three Outside Up",
                    14,
                ),
            })
            
        if detect_three_outside_down(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Three Outside Down",
                "signal": PatternSignal.BEARISH,
                "strength": 14,
                "confidence": calculate_pattern_confidence(
                    "Three Outside Down",
                    14,
                ),
            })
                
    """ Candle Patterns End """
    
    for pattern in patterns:

        adjusted_strength = (
            adjust_pattern_strength(
                signal=pattern["signal"],
                strength=pattern["strength"],
                trend=trend,
            )
        )

        if (
            volume_factor > 1.5
            and pattern["signal"] != PatternSignal.NEUTRAL
        ):

            adjusted_strength += 2

        pattern["strength"] = adjusted_strength
        
        pattern["confidence"] = (
            calculate_pattern_confidence(
                pattern["pattern"],
                pattern["strength"],
            )
        )
    
    patterns.sort(
        key=lambda pattern: (
            pattern["strength"],
            pattern["confidence"]
        ),
        reverse=True,
    )

    patterns = patterns[:5]
    
    score = calculate_pattern_score(patterns)

    return {
        "candlestick_score": score,
        "patterns": patterns,
    }