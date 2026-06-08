from enum import Enum


class PatternSignal(str, Enum):
    BULLISH = "Bullish"
    BEARISH = "Bearish"
    NEUTRAL = "Neutral"


class PatternStrength(Enum):
    WEAK = 5
    MEDIUM = 10
    STRONG = 15