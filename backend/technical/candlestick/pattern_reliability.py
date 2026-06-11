PATTERN_RELIABILITY = {

    # Single Candle
    "Doji": 55,
    "Dragonfly Doji": 68,
    "Gravestone Doji": 68,
    "Long-Legged Doji": 58,

    "Hammer": 72,
    "Inverted Hammer": 70,
    "Hanging Man": 70,
    "Shooting Star": 72,

    "Spinning Top": 52,
    "Marubozu": 75,

    # Double Candle
    "Bullish Engulfing": 78,
    "Bearish Engulfing": 78,

    "Bullish Harami": 70,
    "Bearish Harami": 70,
    "Harami Cross": 72,

    "Piercing Line": 76,
    "Dark Cloud Cover": 76,

    "Tweezer Bottom": 73,
    "Tweezer Top": 73,

    "Matching Low": 68,
    "Matching High": 68,

    "Bullish Kicker": 88,
    "Bearish Kicker": 88,

    # Triple Candle
    "Morning Star": 82,
    "Evening Star": 82,

    "Morning Doji Star": 85,
    "Evening Doji Star": 85,

    "Three White Soldiers": 85,
    "Three Black Crows": 85,

    "Three Inside Up": 80,
    "Three Inside Down": 80,

    "Three Outside Up": 83,
    "Three Outside Down": 83,
}

def get_pattern_reliability(
    pattern_name,
):

    return (
        PATTERN_RELIABILITY.get(
            pattern_name,
            60
        )
    )