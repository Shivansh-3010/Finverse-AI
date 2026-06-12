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

def detect_inverted_hammer(
    open_price,
    high_price,
    low_price,
    close_price,
):
    body = abs(close_price - open_price)

    upper_shadow = (
        high_price -
        max(open_price, close_price)
    )

    lower_shadow = (
        min(open_price, close_price) -
        low_price
    )

    return (
        upper_shadow > body * 2
        and lower_shadow < body
    )
    
def detect_hanging_man(
    open_price,
    high_price,
    low_price,
    close_price,
):
    body = abs(close_price - open_price)

    lower_shadow = (
        min(open_price, close_price)
        - low_price
    )

    upper_shadow = (
        high_price
        - max(open_price, close_price)
    )

    return (
        lower_shadow > body * 2
        and upper_shadow < body
    )
    
def detect_dragonfly_doji(
    open_price,
    high_price,
    low_price,
    close_price,
):
    return (
        abs(open_price - close_price)
        < (high_price - low_price) * 0.05
        and (
            high_price -
            max(open_price, close_price)
        ) < (
            high_price - low_price
        ) * 0.1
    )
    
def detect_gravestone_doji(
    open_price,
    high_price,
    low_price,
    close_price,
):
    return (
        abs(open_price - close_price)
        < (high_price - low_price) * 0.05
        and (
            min(open_price, close_price)
            - low_price
        ) < (
            high_price - low_price
        ) * 0.1
    )
    
def detect_long_legged_doji(
    open_price,
    high_price,
    low_price,
    close_price,
):
    return (
        abs(open_price - close_price)
        < (high_price - low_price) * 0.05
        and (
            high_price - low_price
        ) > abs(close_price - open_price) * 5
    )
    
def detect_marubozu(
    open_price,
    high_price,
    low_price,
    close_price,
):
    body = abs(close_price - open_price)

    upper_shadow = (
        high_price -
        max(open_price, close_price)
    )

    lower_shadow = (
        min(open_price, close_price)
        - low_price
    )

    return (
        upper_shadow < body * 0.05
        and lower_shadow < body * 0.05
    )
    
def detect_bullish_belt_hold(
    open_price,
    high_price,
    low_price,
    close_price,
):
    body = close_price - open_price

    candle_range = (
        high_price - low_price
    )

    return (
        body > 0
        and abs(open_price - low_price)
        <= candle_range * 0.02
        and body >= candle_range * 0.7
    )


def detect_bearish_belt_hold(
    open_price,
    high_price,
    low_price,
    close_price,
):
    body = open_price - close_price

    candle_range = (
        high_price - low_price
    )

    return (
        body > 0
        and abs(open_price - high_price)
        <= candle_range * 0.02
        and body >= candle_range * 0.7
    )


def detect_opening_marubozu(
    open_price,
    high_price,
    low_price,
    close_price,
):
    body = abs(
        close_price - open_price
    )

    upper_shadow = (
        high_price
        - max(open_price, close_price)
    )

    lower_shadow = (
        min(open_price, close_price)
        - low_price
    )

    return (
        lower_shadow <= body * 0.05
        and upper_shadow <= body * 0.25
    )


def detect_closing_marubozu(
    open_price,
    high_price,
    low_price,
    close_price,
):
    body = abs(
        close_price - open_price
    )

    upper_shadow = (
        high_price
        - max(open_price, close_price)
    )

    lower_shadow = (
        min(open_price, close_price)
        - low_price
    )

    return (
        upper_shadow <= body * 0.05
        and lower_shadow <= body * 0.25
    )


def detect_rickshaw_man(
    open_price,
    high_price,
    low_price,
    close_price,
):
    candle_range = (
        high_price - low_price
    )

    body = abs(
        close_price - open_price
    )

    upper_shadow = (
        high_price
        - max(open_price, close_price)
    )

    lower_shadow = (
        min(open_price, close_price)
        - low_price
    )

    return (
        body <= candle_range * 0.05
        and upper_shadow >= candle_range * 0.35
        and lower_shadow >= candle_range * 0.35
    )


def detect_high_wave_candle(
    open_price,
    high_price,
    low_price,
    close_price,
):
    candle_range = (
        high_price - low_price
    )

    body = abs(
        close_price - open_price
    )

    upper_shadow = (
        high_price
        - max(open_price, close_price)
    )

    lower_shadow = (
        min(open_price, close_price)
        - low_price
    )

    return (
        body <= candle_range * 0.2
        and upper_shadow >= body * 2
        and lower_shadow >= body * 2
    )


def detect_paper_umbrella(
    open_price,
    high_price,
    low_price,
    close_price,
):
    body = abs(
        close_price - open_price
    )

    lower_shadow = (
        min(open_price, close_price)
        - low_price
    )

    upper_shadow = (
        high_price
        - max(open_price, close_price)
    )

    return (
        lower_shadow >= body * 2
        and upper_shadow <= body * 0.5
    )


def detect_shaven_head(
    open_price,
    high_price,
    low_price,
    close_price,
):
    return (
        abs(
            high_price
            - max(open_price, close_price)
        )
        <= (
            high_price - low_price
        ) * 0.02
    )


def detect_shaven_bottom(
    open_price,
    high_price,
    low_price,
    close_price,
):
    return (
        abs(
            min(open_price, close_price)
            - low_price
        )
        <= (
            high_price - low_price
        ) * 0.02
    )
    
def detect_long_lower_shadow(
    open_price,
    high_price,
    low_price,
    close_price,
):
    body = abs(
        close_price - open_price
    )

    lower_shadow = (
        min(open_price, close_price)
        - low_price
    )

    return (
        lower_shadow >= body * 3
    )
    
def detect_takuri_line(
    open_price,
    high_price,
    low_price,
    close_price,
):
    body = abs(
        close_price - open_price
    )

    lower_shadow = (
        min(open_price, close_price)
        - low_price
    )

    return (
        lower_shadow >= body * 5
    )
    
def detect_long_upper_shadow(
    open_price,
    high_price,
    low_price,
    close_price,
):
    body = abs(
        close_price - open_price
    )

    upper_shadow = (
        high_price
        - max(open_price, close_price)
    )

    return (
        upper_shadow >= body * 3
    )
    
def detect_bullish_opening_marubozu(
    open_price,
    high_price,
    low_price,
    close_price,
):
    return (
        close_price > open_price
        and abs(
            open_price - low_price
        )
        <= (
            high_price - low_price
        ) * 0.02
    )
    
def detect_bearish_opening_marubozu(
    open_price,
    high_price,
    low_price,
    close_price,
):
    return (
        close_price < open_price
        and abs(
            open_price - high_price
        )
        <= (
            high_price - low_price
        ) * 0.02
    )
    
def detect_bullish_closing_marubozu(
    open_price,
    high_price,
    low_price,
    close_price,
):
    return (
        close_price > open_price
        and abs(
            close_price - high_price
        )
        <= (
            high_price - low_price
        ) * 0.02
    )
    
def detect_bearish_closing_marubozu(
    open_price,
    high_price,
    low_price,
    close_price,
):
    return (
        close_price < open_price
        and abs(
            close_price - low_price
        )
        <= (
            high_price - low_price
        ) * 0.02
    )
    
