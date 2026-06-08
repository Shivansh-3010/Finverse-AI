PATTERN_EXPLANATIONS = {
    "Hammer":
        "Buyers rejected lower prices and pushed the candle higher.",

    "Bullish Engulfing":
        "A bullish candle engulfed the previous bearish candle, indicating buying pressure.",

    "Morning Star":
        "A three-candle reversal pattern suggesting a shift from sellers to buyers.",

    "Shooting Star":
        "Buyers failed to hold higher prices and sellers regained control.",

    "Bearish Engulfing":
        "A bearish candle engulfed the previous bullish candle, indicating selling pressure.",

    "Evening Star":
        "A three-candle reversal pattern suggesting a shift from buyers to sellers.",

    "Doji":
        "Market indecision between buyers and sellers.",

    "Spinning Top":
        "Neither buyers nor sellers gained clear control.",

    "Long Legged Doji":
        "High volatility and strong market indecision."
}


def explain_pattern(pattern_name: str) -> str:
    return PATTERN_EXPLANATIONS.get(
        pattern_name,
        "No explanation available."
    )