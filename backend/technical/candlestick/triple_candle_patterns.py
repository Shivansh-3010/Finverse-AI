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

def detect_three_inside_up(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
):
    return (
        first_close < first_open
        and second_close > second_open
        and third_close > second_close
    )
    
def detect_three_inside_down(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
):
    return (
        first_close > first_open
        and second_close < second_open
        and third_close < second_close
    )
    
def detect_morning_doji_star(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
):
    return (
        first_close < first_open
        and abs(second_open - second_close)
        < abs(first_open - first_close) * 0.1
        and third_close > third_open
    )
    
def detect_evening_doji_star(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
):
    return (
        first_close > first_open
        and abs(second_open - second_close)
        < abs(first_open - first_close) * 0.1
        and third_close < third_open
    )
    
def detect_three_outside_up(
    first_open,
    first_close,
    second_open,
    second_close,
    third_close,
):
    return (
        first_close < first_open
        and second_close > first_open
        and third_close > second_close
    )
    
def detect_three_outside_down(
    first_open,
    first_close,
    second_open,
    second_close,
    third_close,
):
    return (
        first_close > first_open
        and second_close < first_open
        and third_close < second_close
    )
    
