import math
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
    
    detect_bullish_belt_hold,
    detect_bearish_belt_hold,
    detect_opening_marubozu,
    detect_closing_marubozu,
    detect_rickshaw_man,
    detect_high_wave_candle,
    detect_paper_umbrella,
    detect_shaven_head,
    detect_shaven_bottom,

    detect_takuri_line,
    detect_long_lower_shadow,
    detect_long_upper_shadow,
    detect_bullish_opening_marubozu,
    detect_bearish_opening_marubozu,
    detect_bullish_closing_marubozu,
    detect_bearish_closing_marubozu,

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
    
    detect_bullish_meeting_lines,
    detect_bearish_meeting_lines,

    detect_bullish_separating_lines,
    detect_bearish_separating_lines,

    detect_bullish_counterattack,
    detect_bearish_counterattack,

    detect_on_neck_pattern,
    detect_in_neck_pattern,
    detect_thrusting_pattern,

    detect_homing_pigeon,

    detect_kicking_bullish,
    detect_kicking_bearish,

    detect_kicking_by_length_bullish,
    detect_kicking_by_length_bearish,

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
    
    detect_tri_star_bullish,
    detect_tri_star_bearish,

    detect_advance_block,
    detect_deliberation,

    detect_identical_three_crows,

    detect_three_stars_in_the_south,

    detect_three_river_bottom,
    detect_three_river_top,

    detect_bullish_doji_star,
    detect_bearish_doji_star,
    
    detect_rising_three_methods,
    detect_falling_three_methods,

    detect_bullish_abandoned_baby,
    detect_bearish_abandoned_baby,

    detect_bullish_tasuki_gap,
    detect_bearish_tasuki_gap,

    detect_bullish_window,
    detect_bearish_window,

    detect_upside_gap_two_crows,

    detect_stick_sandwich,

    detect_bullish_mat_hold,
    detect_bearish_mat_hold,

    detect_bullish_breakaway,
    detect_bearish_breakaway,

    detect_side_by_side_white_lines,

    detect_ladder_bottom,

    detect_concealing_baby_swallow,

    detect_unique_three_river,

    detect_matching_three_crows,

    detect_gap_three_methods_bullish,
    detect_gap_three_methods_bearish,

    detect_three_line_strike,

    detect_three_gap_ups,
    detect_three_gap_downs,

    detect_gapping_side_by_side_white_lines,
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
from .pattern_reliability import (
    get_pattern_reliability,
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

    valid_records = []

    for record in records:

        if not (
            math.isnan(float(record.open))
            or math.isnan(float(record.high))
            or math.isnan(float(record.low))
            or math.isnan(float(record.close))
        ):
            valid_records.append(record)

    if not valid_records:
        return {
            "candlestick_score": 0,
            "patterns": []
        }

    latest = valid_records[0]

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
        
    if detect_takuri_line(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Takuri Line",
            "signal": PatternSignal.BULLISH,
            "strength": 9,
        })

    if detect_long_lower_shadow(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Long Lower Shadow",
            "signal": PatternSignal.BULLISH,
            "strength": 6,
        })

    if detect_long_upper_shadow(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Long Upper Shadow",
            "signal": PatternSignal.BEARISH,
            "strength": 6,
        })

    if detect_rickshaw_man(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Rickshaw Man",
            "signal": PatternSignal.NEUTRAL,
            "strength": 5,
        })
        
    if detect_high_wave_candle(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "High Wave Candle",
            "signal": PatternSignal.NEUTRAL,
            "strength": 5,
        })

    if detect_paper_umbrella(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Paper Umbrella",
            "signal": PatternSignal.BULLISH,
            "strength": 7,
        })

    if detect_bullish_belt_hold(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Bullish Belt Hold",
            "signal": PatternSignal.BULLISH,
            "strength": 8,
        })

    if detect_bearish_belt_hold(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Bearish Belt Hold",
            "signal": PatternSignal.BEARISH,
            "strength": 8,
        })

    if detect_shaven_head(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Shaven Head",
            "signal": PatternSignal.BEARISH,
            "strength": 6,
        })
        
    if detect_shaven_bottom(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Shaven Bottom",
            "signal": PatternSignal.BULLISH,
            "strength": 6,
        })

    if detect_opening_marubozu(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Opening Marubozu",
            "signal": PatternSignal.NEUTRAL,
            "strength": 7,
        })

    if detect_closing_marubozu(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Closing Marubozu",
            "signal": PatternSignal.NEUTRAL,
            "strength": 7,
        })

    if detect_bullish_opening_marubozu(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Bullish Opening Marubozu",
            "signal": PatternSignal.BULLISH,
            "strength": 8,
        })

    if detect_bearish_opening_marubozu(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Bearish Opening Marubozu",
            "signal": PatternSignal.BEARISH,
            "strength": 8,
        })

    if detect_bullish_closing_marubozu(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Bullish Closing Marubozu",
            "signal": PatternSignal.BULLISH,
            "strength": 8,
        })

    if detect_bearish_closing_marubozu(
        open_price,
        high_price,
        low_price,
        close_price,
    ):
        patterns.append({
            "pattern": "Bearish Closing Marubozu",
            "signal": PatternSignal.BEARISH,
            "strength": 8,
        })
        
        
    """ Double Candle Patterns """
    
    if len(valid_records) >= 2:

        previous = valid_records[1]

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
            
        if detect_bullish_meeting_lines(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bullish Meeting Lines",
                "signal": PatternSignal.BULLISH,
                "strength": 9,
            })

        if detect_bearish_meeting_lines(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bearish Meeting Lines",
                "signal": PatternSignal.BEARISH,
                "strength": 9,
            })

        if detect_bullish_separating_lines(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bullish Separating Lines",
                "signal": PatternSignal.BULLISH,
                "strength": 10,
            })

        if detect_bearish_separating_lines(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bearish Separating Lines",
                "signal": PatternSignal.BEARISH,
                "strength": 10,
            })
            
        if detect_bullish_counterattack(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bullish Counterattack",
                "signal": PatternSignal.BULLISH,
                "strength": 10,
            })

        if detect_bearish_counterattack(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Bearish Counterattack",
                "signal": PatternSignal.BEARISH,
                "strength": 10,
            })

        if detect_on_neck_pattern(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "On Neck Pattern",
                "signal": PatternSignal.BEARISH,
                "strength": 8,
            })

        if detect_in_neck_pattern(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "In Neck Pattern",
                "signal": PatternSignal.BEARISH,
                "strength": 8,
            })

        if detect_thrusting_pattern(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Thrusting Pattern",
                "signal": PatternSignal.BEARISH,
                "strength": 9,
            })
            
        if detect_homing_pigeon(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Homing Pigeon",
                "signal": PatternSignal.BULLISH,
                "strength": 8,
            })

        if detect_kicking_bullish(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Kicking Bullish",
                "signal": PatternSignal.BULLISH,
                "strength": 12,
            })

        if detect_kicking_bearish(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Kicking Bearish",
                "signal": PatternSignal.BEARISH,
                "strength": 12,
            })

        if detect_kicking_by_length_bullish(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Kicking By Length Bullish",
                "signal": PatternSignal.BULLISH,
                "strength": 13,
            })

        if detect_kicking_by_length_bearish(
            prev_open=float(previous.open),
            prev_close=float(previous.close),
            curr_open=open_price,
            curr_close=close_price,
        ):
            patterns.append({
                "pattern": "Kicking By Length Bearish",
                "signal": PatternSignal.BEARISH,
                "strength": 13,
            })
            
    """ Triple Candle Patterns """
            
    if len(valid_records) >= 3:

        third = valid_records[0]
        second = valid_records[1]
        first = valid_records[2]

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
            
        if detect_tri_star_bullish(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Tri Star Bullish",
                "signal": PatternSignal.BULLISH,
                "strength": 14,
            })
            
        if detect_tri_star_bearish(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Tri Star Bearish",
                "signal": PatternSignal.BEARISH,
                "strength": 14,
            })
            
        if detect_advance_block(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Advance Block",
                "signal": PatternSignal.BEARISH,
                "strength": 12,
            })
            
        if detect_deliberation(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Deliberation",
                "signal": PatternSignal.BEARISH,
                "strength": 12,
            })
            
        if detect_identical_three_crows(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Identical Three Crows",
                "signal": PatternSignal.BEARISH,
                "strength": 15,
            })
            
        if detect_three_stars_in_the_south(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Three Stars In The South",
                "signal": PatternSignal.BULLISH,
                "strength": 13,
            })
            
        if detect_three_river_bottom(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Three River Bottom",
                "signal": PatternSignal.BULLISH,
                "strength": 12,
            })
            
        if detect_three_river_top(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Three River Top",
                "signal": PatternSignal.BEARISH,
                "strength": 12,
            })
            
        if detect_bullish_doji_star(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Bullish Doji Star",
                "signal": PatternSignal.BULLISH,
                "strength": 13,
            })
            
        if detect_bearish_doji_star(
            first_open=float(first.open),
            first_close=float(first.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(third.open),
            third_close=float(third.close),
        ):
            patterns.append({
                "pattern": "Bearish Doji Star",
                "signal": PatternSignal.BEARISH,
                "strength": 13,
            })
            
    """ Advanced Candle Patterns """
    
    if len(valid_records) >= 5:

        first = valid_records[4]
        second = valid_records[3]
        third = valid_records[2]
        fourth = valid_records[1]
        fifth = valid_records[0]
        
        if detect_rising_three_methods(
            first_open=float(fifth.open),
            first_close=float(fifth.close),
            second_open=float(fourth.open),
            second_close=float(fourth.close),
            third_open=float(third.open),
            third_close=float(third.close),
            fourth_open=float(second.open),
            fourth_close=float(second.close),
            fifth_open=float(first.open),
            fifth_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Rising Three Methods",
                "signal": PatternSignal.BULLISH,
                "strength": 15,
            })

        if detect_falling_three_methods(
            first_open=float(fifth.open),
            first_close=float(fifth.close),
            second_open=float(fourth.open),
            second_close=float(fourth.close),
            third_open=float(third.open),
            third_close=float(third.close),
            fourth_open=float(second.open),
            fourth_close=float(second.close),
            fifth_open=float(first.open),
            fifth_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Falling Three Methods",
                "signal": PatternSignal.BEARISH,
                "strength": 15,
            })

        if detect_bullish_mat_hold(
            first_open=float(fifth.open),
            first_close=float(fifth.close),
            second_open=float(fourth.open),
            second_close=float(fourth.close),
            third_open=float(third.open),
            third_close=float(third.close),
            fourth_open=float(second.open),
            fourth_close=float(second.close),
            fifth_open=float(first.open),
            fifth_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Bullish Mat Hold",
                "signal": PatternSignal.BULLISH,
                "strength": 16,
            })

        if detect_bearish_mat_hold(
            first_open=float(fifth.open),
            first_close=float(fifth.close),
            second_open=float(fourth.open),
            second_close=float(fourth.close),
            third_open=float(third.open),
            third_close=float(third.close),
            fourth_open=float(second.open),
            fourth_close=float(second.close),
            fifth_open=float(first.open),
            fifth_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Bearish Mat Hold",
                "signal": PatternSignal.BEARISH,
                "strength": 16,
            })

        if detect_three_line_strike(
            first_open=float(fourth.open),
            first_close=float(fourth.close),
            second_open=float(third.open),
            second_close=float(third.close),
            third_open=float(second.open),
            third_close=float(second.close),
            fourth_open=float(first.open),
            fourth_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Three Line Strike",
                "signal": PatternSignal.BULLISH,
                "strength": 18,
            })
                
        if detect_bullish_abandoned_baby(
            first_open=float(third.open),
            first_close=float(third.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(first.open),
            third_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Bullish Abandoned Baby",
                "signal": PatternSignal.BULLISH,
                "strength": 16,
            })

        if detect_bearish_abandoned_baby(
            first_open=float(third.open),
            first_close=float(third.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(first.open),
            third_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Bearish Abandoned Baby",
                "signal": PatternSignal.BEARISH,
                "strength": 16,
            })

        if detect_bullish_breakaway(
            first_open=float(fifth.open),
            first_close=float(fifth.close),
            fifth_open=float(first.open),
            fifth_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Bullish Breakaway",
                "signal": PatternSignal.BULLISH,
                "strength": 15,
            })

        if detect_bearish_breakaway(
            first_open=float(fifth.open),
            first_close=float(fifth.close),
            fifth_open=float(first.open),
            fifth_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Bearish Breakaway",
                "signal": PatternSignal.BEARISH,
                "strength": 15,
            })

        if detect_upside_gap_two_crows(
            first_open=float(third.open),
            first_close=float(third.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(first.open),
            third_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Upside Gap Two Crows",
                "signal": PatternSignal.BEARISH,
                "strength": 15,
            })
            
        if detect_bullish_tasuki_gap(
            first_open=float(third.open),
            first_close=float(third.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(first.open),
            third_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Bullish Tasuki Gap",
                "signal": PatternSignal.BULLISH,
                "strength": 14,
            })

        if detect_bearish_tasuki_gap(
            first_open=float(third.open),
            first_close=float(third.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(first.open),
            third_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Bearish Tasuki Gap",
                "signal": PatternSignal.BEARISH,
                "strength": 14,
            })

        if detect_bullish_window(
            first_high=float(second.high),
            second_low=float(first.low),
        ):
            patterns.append({
                "pattern": "Bullish Window",
                "signal": PatternSignal.BULLISH,
                "strength": 10,
            })

        if detect_bearish_window(
            first_low=float(second.low),
            second_high=float(first.high),
        ):
            patterns.append({
                "pattern": "Bearish Window",
                "signal": PatternSignal.BEARISH,
                "strength": 10,
            })

        if detect_gap_three_methods_bullish(
            first_close=float(third.close),
            second_open=float(second.open),
            third_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Gap Three Methods Bullish",
                "signal": PatternSignal.BULLISH,
                "strength": 13,
            })

        if detect_gap_three_methods_bearish(
            first_close=float(third.close),
            second_open=float(second.open),
            third_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Gap Three Methods Bearish",
                "signal": PatternSignal.BEARISH,
                "strength": 13,
            })
            
        if detect_stick_sandwich(
            first_open=float(third.open),
            first_close=float(third.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(first.open),
            third_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Stick Sandwich",
                "signal": PatternSignal.BULLISH,
                "strength": 14,
            })

        if detect_side_by_side_white_lines(
            first_open=float(second.open),
            first_close=float(second.close),
            second_open=float(first.open),
            second_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Side By Side White Lines",
                "signal": PatternSignal.BULLISH,
                "strength": 12,
            })

        if detect_gapping_side_by_side_white_lines(
            first_open=float(second.open),
            first_close=float(second.close),
            second_open=float(first.open),
            second_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Gapping Side By Side White Lines",
                "signal": PatternSignal.BULLISH,
                "strength": 13,
            })

        if detect_matching_three_crows(
            first_close=float(third.close),
            second_close=float(second.close),
            third_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Matching Three Crows",
                "signal": PatternSignal.BEARISH,
                "strength": 15,
            })
            
        if detect_ladder_bottom(
            first_close=float(fifth.close),
            second_close=float(fourth.close),
            third_close=float(third.close),
            fourth_close=float(second.close),
            fifth_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Ladder Bottom",
                "signal": PatternSignal.BULLISH,
                "strength": 15,
            })

        if detect_concealing_baby_swallow(
            first_open=float(second.open),
            first_close=float(second.close),
            second_open=float(first.open),
            second_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Concealing Baby Swallow",
                "signal": PatternSignal.BULLISH,
                "strength": 17,
            })

        if detect_unique_three_river(
            first_open=float(third.open),
            first_close=float(third.close),
            second_open=float(second.open),
            second_close=float(second.close),
            third_open=float(first.open),
            third_close=float(first.close),
        ):
            patterns.append({
                "pattern": "Unique Three River",
                "signal": PatternSignal.BULLISH,
                "strength": 14,
            })

        if detect_three_gap_ups(
            first_high=float(third.high),
            second_low=float(second.low),
            second_high=float(second.high),
            third_low=float(first.low),
        ):
            patterns.append({
                "pattern": "Three Gap Ups",
                "signal": PatternSignal.BULLISH,
                "strength": 15,
            })

        if detect_three_gap_downs(
            first_low=float(third.low),
            second_high=float(second.high),
            second_low=float(second.low),
            third_high=float(first.high),
        ):
            patterns.append({
                "pattern": "Three Gap Downs",
                "signal": PatternSignal.BEARISH,
                "strength": 15,
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
        
        base_confidence = (
            calculate_pattern_confidence(
                pattern["pattern"],
                pattern["strength"],
            )
        )

        reliability = (
            get_pattern_reliability(
                pattern["pattern"]
            )
        )

        pattern["confidence"] = (
            base_confidence + reliability
        ) / 2
    
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