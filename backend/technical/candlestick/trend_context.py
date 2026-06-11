def determine_trend(closes):

    if len(closes) < 20:
        return "unknown"

    sma20 = sum(closes[-20:]) / 20

    latest_close = closes[-1]

    if latest_close > sma20:
        return "uptrend"

    if latest_close < sma20:
        return "downtrend"

    return "sideways"