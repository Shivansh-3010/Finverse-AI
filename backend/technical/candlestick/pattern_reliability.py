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

    "Takuri Line": 74,

    "Long Lower Shadow": 62,
    "Long Upper Shadow": 62,

    "Bullish Belt Hold": 78,
    "Bearish Belt Hold": 78,

    "Rickshaw Man": 60,
    "High Wave Candle": 58,

    "Paper Umbrella": 72,

    "Shaven Head": 60,
    "Shaven Bottom": 60,

    "Opening Marubozu": 70,
    "Closing Marubozu": 70,

    "Bullish Opening Marubozu": 74,
    "Bearish Opening Marubozu": 74,

    "Bullish Closing Marubozu": 74,
    "Bearish Closing Marubozu": 74,

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

    "Bullish Meeting Lines": 70,
    "Bearish Meeting Lines": 70,

    "Bullish Separating Lines": 76,
    "Bearish Separating Lines": 76,

    "Bullish Counterattack": 78,
    "Bearish Counterattack": 78,

    "On Neck Pattern": 68,
    "In Neck Pattern": 70,
    "Thrusting Pattern": 72,

    "Homing Pigeon": 72,

    "Kicking Bullish": 88,
    "Kicking Bearish": 88,

    "Kicking By Length Bullish": 92,
    "Kicking By Length Bearish": 92,

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

    "Tri Star Bullish": 88,
    "Tri Star Bearish": 88,

    "Advance Block": 78,
    "Deliberation": 80,

    "Identical Three Crows": 90,

    "Three Stars In The South": 82,

    "Three River Bottom": 80,
    "Three River Top": 80,

    "Bullish Doji Star": 84,
    "Bearish Doji Star": 84,
    
    # Advanced Patterns

    "Rising Three Methods": 85,
    "Falling Three Methods": 85,

    "Bullish Abandoned Baby": 92,
    "Bearish Abandoned Baby": 92,

    "Bullish Tasuki Gap": 82,
    "Bearish Tasuki Gap": 82,

    "Bullish Window": 72,
    "Bearish Window": 72,

    "Upside Gap Two Crows": 84,

    "Stick Sandwich": 80,

    "Bullish Mat Hold": 88,
    "Bearish Mat Hold": 88,

    "Bullish Breakaway": 85,
    "Bearish Breakaway": 85,

    "Side By Side White Lines": 76,

    "Ladder Bottom": 82,

    "Concealing Baby Swallow": 92,

    "Unique Three River": 82,

    "Matching Three Crows": 84,

    "Gap Three Methods Bullish": 80,
    "Gap Three Methods Bearish": 80,

    "Three Line Strike": 95,

    "Three Gap Ups": 84,
    "Three Gap Downs": 84,

    "Gapping Side By Side White Lines": 82,
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