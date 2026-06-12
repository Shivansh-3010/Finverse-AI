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
    
def detect_bullish_meeting_lines(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
    tolerance=0.002,
):
    return (
        prev_close < prev_open
        and curr_close > curr_open
        and abs(
            prev_close - curr_close
        )
        <= max(
            abs(prev_close),
            abs(curr_close),
        ) * tolerance
    )


def detect_bearish_meeting_lines(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
    tolerance=0.002,
):
    return (
        prev_close > prev_open
        and curr_close < curr_open
        and abs(
            prev_close - curr_close
        )
        <= max(
            abs(prev_close),
            abs(curr_close),
        ) * tolerance
    )


def detect_bullish_separating_lines(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
    tolerance=0.002,
):
    return (
        prev_close < prev_open
        and curr_close > curr_open
        and abs(
            prev_open - curr_open
        )
        <= max(
            abs(prev_open),
            abs(curr_open),
        ) * tolerance
    )


def detect_bearish_separating_lines(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
    tolerance=0.002,
):
    return (
        prev_close > prev_open
        and curr_close < curr_open
        and abs(
            prev_open - curr_open
        )
        <= max(
            abs(prev_open),
            abs(curr_open),
        ) * tolerance
    )


def detect_bullish_counterattack(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
    tolerance=0.002,
):
    return (
        prev_close < prev_open
        and curr_close > curr_open
        and abs(
            prev_close - curr_close
        )
        <= max(
            abs(prev_close),
            abs(curr_close),
        ) * tolerance
    )


def detect_bearish_counterattack(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
    tolerance=0.002,
):
    return (
        prev_close > prev_open
        and curr_close < curr_open
        and abs(
            prev_close - curr_close
        )
        <= max(
            abs(prev_close),
            abs(curr_close),
        ) * tolerance
    )


def detect_on_neck_pattern(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    return (
        prev_close < prev_open
        and curr_open < prev_close
        and curr_close >= prev_close
        and curr_close <= prev_close * 1.01
    )


def detect_in_neck_pattern(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    return (
        prev_close < prev_open
        and curr_open < prev_close
        and curr_close > prev_close
        and curr_close < (
            prev_open + prev_close
        ) / 2
    )


def detect_thrusting_pattern(
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
        and curr_close > prev_close
        and curr_close < midpoint
    )


def detect_homing_pigeon(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    return (
        prev_close < prev_open
        and curr_open > prev_close
        and curr_close < prev_open
        and abs(
            curr_close - curr_open
        )
        < abs(
            prev_close - prev_open
        )
    )
    
def detect_kicking_bullish(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    return (
        prev_close < prev_open
        and curr_close > curr_open
        and curr_open > prev_open
    )
    
def detect_kicking_bearish(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    return (
        prev_close > prev_open
        and curr_close < curr_open
        and curr_open < prev_open
    )
    
def detect_kicking_by_length_bullish(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    previous_body = abs(
        prev_close - prev_open
    )

    current_body = abs(
        curr_close - curr_open
    )

    return (
        detect_kicking_bullish(
            prev_open,
            prev_close,
            curr_open,
            curr_close,
        )
        and current_body > previous_body
    )
    
def detect_kicking_by_length_bearish(
    prev_open,
    prev_close,
    curr_open,
    curr_close,
):
    previous_body = abs(
        prev_close - prev_open
    )

    current_body = abs(
        curr_close - curr_open
    )

    return (
        detect_kicking_bearish(
            prev_open,
            prev_close,
            curr_open,
            curr_close,
        )
        and current_body > previous_body
    )
    
