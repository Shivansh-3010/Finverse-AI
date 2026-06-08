from .pattern_types import PatternSignal, PatternStrength


PATTERN_REGISTRY = {
    # Bullish Patterns
    "Hammer": {
        "signal": PatternSignal.BULLISH,
        "strength": 8,
    },
    "Bullish Engulfing": {
        "signal": PatternSignal.BULLISH,
        "strength": 10,
    },
    "Morning Star": {
        "signal": PatternSignal.BULLISH,
        "strength": 15,
    },
    "Piercing Pattern": {
        "signal": PatternSignal.BULLISH,
        "strength": 10,
    },
    "Three White Soldiers": {
        "signal": PatternSignal.BULLISH,
        "strength": 15,
    },

    # Bearish Patterns
    "Shooting Star": {
        "signal": PatternSignal.BEARISH,
        "strength": 8,
    },
    "Bearish Engulfing": {
        "signal": PatternSignal.BEARISH,
        "strength": 10,
    },
    "Evening Star": {
        "signal": PatternSignal.BEARISH,
        "strength": 15,
    },
    "Dark Cloud Cover": {
        "signal": PatternSignal.BEARISH,
        "strength": 10,
    },
    "Three Black Crows": {
        "signal": PatternSignal.BEARISH,
        "strength": 15,
    },

    # Neutral Patterns
    "Doji": {
        "signal": PatternSignal.NEUTRAL,
        "strength": 5,
    },
    "Spinning Top": {
        "signal": PatternSignal.NEUTRAL,
        "strength": 5,
    },
    "Long Legged Doji": {
        "signal": PatternSignal.NEUTRAL,
        "strength": 5,
    },
}