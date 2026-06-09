import pandas as pd

from .models import PatternResult


def detect_doji(
    open_price: float,
    high_price: float,
    low_price: float,
    close_price: float,
) -> bool:
    """
    Detect Doji candle.

    Body should be very small compared to total range.
    """

    candle_range = high_price - low_price

    if candle_range == 0:
        return False

    body_size = abs(close_price - open_price)

    return (body_size / candle_range) < 0.1

def detect_hammer(
    open_price: float,
    high_price: float,
    low_price: float,
    close_price: float,
) -> bool:
    """
    Detect Hammer candle.
    """

    body = abs(close_price - open_price)

    lower_shadow = min(open_price, close_price) - low_price

    upper_shadow = high_price - max(open_price, close_price)

    if body == 0:
        return False

    return (
        lower_shadow >= body * 2
        and upper_shadow <= body
    )
    
def detect_bullish_engulfing(
    prev_open: float,
    prev_close: float,
    curr_open: float,
    curr_close: float,
) -> bool:
    """
    Detect Bullish Engulfing pattern.
    """

    previous_bearish = prev_close < prev_open

    current_bullish = curr_close > curr_open

    engulfing = (
        curr_open < prev_close
        and curr_close > prev_open
    )

    return (
        previous_bearish
        and current_bullish
        and engulfing
    )
    
def detect_bearish_engulfing(
    prev_open: float,
    prev_close: float,
    curr_open: float,
    curr_close: float,
) -> bool:
    """
    Detect Bearish Engulfing pattern.
    """

    previous_bullish = prev_close > prev_open

    current_bearish = curr_close < curr_open

    engulfing = (
        curr_open > prev_close
        and curr_close < prev_open
    )

    return (
        previous_bullish
        and current_bearish
        and engulfing
    )
    
def detect_morning_star(
    first_open: float,
    first_close: float,
    second_open: float,
    second_close: float,
    third_open: float,
    third_close: float,
) -> bool:
    """
    Detect Morning Star pattern.
    """

    first_bearish = first_close < first_open

    second_body = abs(
        second_close - second_open
    )

    first_body = abs(
        first_close - first_open
    )

    small_middle_candle = (
        second_body < first_body * 0.5
    )

    third_bullish = third_close > third_open

    recovery = (
        third_close >
        (first_open + first_close) / 2
    )

    return (
        first_bearish
        and small_middle_candle
        and third_bullish
        and recovery
    )
    
def detect_evening_star(
    first_open: float,
    first_close: float,
    second_open: float,
    second_close: float,
    third_open: float,
    third_close: float,
) -> bool:
    """
    Detect Evening Star pattern.
    """

    first_bullish = first_close > first_open

    second_body = abs(
        second_close - second_open
    )

    first_body = abs(
        first_close - first_open
    )

    small_middle_candle = (
        second_body < first_body * 0.5
    )

    third_bearish = third_close < third_open

    breakdown = (
        third_close <
        (first_open + first_close) / 2
    )

    return (
        first_bullish
        and small_middle_candle
        and third_bearish
        and breakdown
    )


def detect_three_white_soldiers(
    first_open: float,
    first_close: float,
    second_open: float,
    second_close: float,
    third_open: float,
    third_close: float,
) -> bool:
    """
    Detect Three White Soldiers.
    """

    return (
        first_close > first_open
        and second_close > second_open
        and third_close > third_open
        and second_close > first_close
        and third_close > second_close
    )


def detect_three_black_crows(
    first_open: float,
    first_close: float,
    second_open: float,
    second_close: float,
    third_open: float,
    third_close: float,
) -> bool:
    """
    Detect Three Black Crows.
    """

    return (
        first_close < first_open
        and second_close < second_open
        and third_close < third_open
        and second_close < first_close
        and third_close < second_close
    )
    
def detect_shooting_star(
    open_price: float,
    high_price: float,
    low_price: float,
    close_price: float,
) -> bool:
    """
    Detect Shooting Star candle.
    """

    body = abs(close_price - open_price)

    upper_shadow = (
        high_price - max(open_price, close_price)
    )

    lower_shadow = (
        min(open_price, close_price) - low_price
    )

    if body == 0:
        return False

    return (
        upper_shadow >= body * 2
        and lower_shadow <= body
    )
    
def detect_spinning_top(
    open_price: float,
    high_price: float,
    low_price: float,
    close_price: float,
) -> bool:
    """
    Detect Spinning Top candle.
    """

    candle_range = high_price - low_price

    if candle_range == 0:
        return False

    body = abs(close_price - open_price)

    body_ratio = body / candle_range

    return 0.10 <= body_ratio <= 0.30