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