def detect_rising_three_methods(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
    fourth_open,
    fourth_close,
    fifth_open,
    fifth_close,
):
    return (
        first_close > first_open
        and second_close < second_open
        and third_close < third_open
        and fourth_close < fourth_open
        and fifth_close > fifth_open
        and fifth_close > first_close
    )


def detect_falling_three_methods(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
    fourth_open,
    fourth_close,
    fifth_open,
    fifth_close,
):
    return (
        first_close < first_open
        and second_close > second_open
        and third_close > third_open
        and fourth_close > fourth_open
        and fifth_close < fifth_open
        and fifth_close < first_close
    )


def detect_bullish_abandoned_baby(
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
        <= abs(second_open) * 0.002
        and third_close > third_open
    )


def detect_bearish_abandoned_baby(
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
        <= abs(second_open) * 0.002
        and third_close < third_open
    )


def detect_bullish_tasuki_gap(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
):
    return (
        first_close > first_open
        and second_open > first_close
        and second_close > second_open
        and third_close < third_open
    )


def detect_bearish_tasuki_gap(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
):
    return (
        first_close < first_open
        and second_open < first_close
        and second_close < second_open
        and third_close > third_open
    )
    
def detect_bullish_window(
    first_high,
    second_low,
):
    return second_low > first_high


def detect_bearish_window(
    first_low,
    second_high,
):
    return second_high < first_low


def detect_upside_gap_two_crows(
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
        and third_close < third_open
        and second_open > first_close
        and third_open > second_open
    )


def detect_stick_sandwich(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
    tolerance=0.002,
):
    return (
        first_close < first_open
        and second_close > second_open
        and third_close < third_open
        and abs(
            first_close - third_close
        )
        <= abs(first_close) * tolerance
    )


def detect_bullish_mat_hold(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
    fourth_open,
    fourth_close,
    fifth_open,
    fifth_close,
):
    return (
        first_close > first_open
        and second_close < second_open
        and third_close < third_open
        and fourth_close < fourth_open
        and fifth_close > fifth_open
        and fifth_close > first_close
    )


def detect_bearish_mat_hold(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
    fourth_open,
    fourth_close,
    fifth_open,
    fifth_close,
):
    return (
        first_close < first_open
        and second_close > second_open
        and third_close > third_open
        and fourth_close > fourth_open
        and fifth_close < fifth_open
        and fifth_close < first_close
    )
    
def detect_bullish_breakaway(
    first_open,
    first_close,
    fifth_open,
    fifth_close,
):
    return (
        first_close < first_open
        and fifth_close > fifth_open
    )


def detect_bearish_breakaway(
    first_open,
    first_close,
    fifth_open,
    fifth_close,
):
    return (
        first_close > first_open
        and fifth_close < fifth_open
    )


def detect_side_by_side_white_lines(
    first_open,
    first_close,
    second_open,
    second_close,
):
    return (
        first_close > first_open
        and second_close > second_open
        and abs(
            first_open - second_open
        ) <= abs(first_open) * 0.01
    )


def detect_ladder_bottom(
    first_close,
    second_close,
    third_close,
    fourth_close,
    fifth_close,
):
    return (
        first_close > second_close
        > third_close > fourth_close
        and fifth_close > fourth_close
    )


def detect_concealing_baby_swallow(
    first_open,
    first_close,
    second_open,
    second_close,
):
    return (
        first_close < first_open
        and second_close < second_open
    )


def detect_unique_three_river(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
):
    return (
        first_close < first_open
        and second_close < second_open
        and third_close > third_open
    )


def detect_matching_three_crows(
    first_close,
    second_close,
    third_close,
):
    return (
        abs(first_close - second_close)
        <= abs(first_close) * 0.01
        and abs(second_close - third_close)
        <= abs(second_close) * 0.01
    )


def detect_gap_three_methods_bullish(
    first_close,
    second_open,
    third_close,
):
    return (
        second_open > first_close
        and third_close > first_close
    )


def detect_gap_three_methods_bearish(
    first_close,
    second_open,
    third_close,
):
    return (
        second_open < first_close
        and third_close < first_close
    )


def detect_three_line_strike(
    first_open,
    first_close,
    second_open,
    second_close,
    third_open,
    third_close,
    fourth_open,
    fourth_close,
):
    return (
        first_close > first_open
        and second_close > second_open
        and third_close > third_open
        and fourth_close < fourth_open
    )
    
def detect_three_gap_ups(
    first_high,
    second_low,
    second_high,
    third_low,
):
    return (
        second_low > first_high
        and third_low > second_high
    )
    
def detect_three_gap_downs(
    first_low,
    second_high,
    second_low,
    third_high,
):
    return (
        second_high < first_low
        and third_high < second_low
    )
    
def detect_gapping_side_by_side_white_lines(
    first_open,
    first_close,
    second_open,
    second_close,
):
    return (
        first_close > first_open
        and second_close > second_open
        and abs(
            first_open - second_open
        )
        <= abs(first_open) * 0.01
    )