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
    
def detect_bullish_harami(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    return (
        prev_close < prev_open
        and curr_open > prev_close
        and curr_close < prev_open
    )
    
def detect_bearish_harami(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    return (
        prev_close > prev_open
        and curr_open < prev_close
        and curr_close > prev_open
    )
    
def detect_piercing_line(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    midpoint = (
        prev_open + prev_close
    ) / 2

    return (
        prev_close < prev_open
        and curr_open < prev_close
        and curr_close > midpoint
    )

def detect_dark_cloud_cover(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    midpoint = (
        prev_open + prev_close
    ) / 2

    return (
        prev_close > prev_open
        and curr_open > prev_close
        and curr_close < midpoint
    )
    
def detect_tweezer_top(
    prev_high,
    curr_high,
    tolerance=0.001,
):
    return (
        abs(prev_high - curr_high)
        <= max(prev_high, curr_high)
        * tolerance
    )
    
def detect_tweezer_bottom(
    prev_low,
    curr_low,
    tolerance=0.001,
):
    return (
        abs(prev_low - curr_low)
        <= max(prev_low, curr_low)
        * tolerance
    )
    
def detect_harami_cross(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    return (
        abs(curr_open - curr_close)
        < abs(prev_open - prev_close) * 0.1
    )
    
def detect_matching_high(
    prev_close,
    curr_close,
    tolerance=0.002,
):
    return (
        abs(prev_close - curr_close)
        <= max(prev_close, curr_close)
        * tolerance
    )
    
def detect_matching_low(
    prev_low,
    curr_low,
    tolerance=0.002,
):
    return (
        abs(prev_low - curr_low)
        <= max(prev_low, curr_low)
        * tolerance
    )
    
def detect_bullish_kicker(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    return (
        prev_close < prev_open
        and curr_open > prev_open
        and curr_close > curr_open
    )
    
def detect_bearish_kicker(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    return (
        prev_close > prev_open
        and curr_open < prev_open
        and curr_close < curr_open
    )
    
