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
    
