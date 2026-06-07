def calculate_technical_score(
    rsi: float,
    macd_bullish: bool,
    ema_bullish: bool
) -> dict:
    """
    Simple MVP technical scoring engine.
    Score range: 0-100
    """

    score = 50
    reasons = []

    # RSI
    if rsi < 30:
        score += 10
        reasons.append("RSI oversold (bullish)")
    elif rsi > 70:
        score -= 10
        reasons.append("RSI overbought (bearish)")

    # MACD
    if macd_bullish:
        score += 15
        reasons.append("MACD bullish crossover")

    # EMA Trend
    if ema_bullish:
        score += 10
        reasons.append("EMA trend bullish")

    score = max(0, min(score, 100))

    return {
        "technical_score": score,
        "reasons": reasons
    }