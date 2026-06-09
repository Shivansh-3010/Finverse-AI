def generate_candlestick_features(
    analysis_result: dict,
):
    """
    Generate ML-ready candlestick features
    from analyzed pattern results.
    """

    patterns = analysis_result.get(
        "patterns",
        []
    )

    features = {
        "patterns_detected": len(patterns),

        "pattern_score":
            analysis_result.get(
                "candlestick_score",
                50,
            ),

        "pattern_strength": 0,

        "bullish_pattern_present": 0,
        "bearish_pattern_present": 0,
        "neutral_pattern_present": 0,

        "doji_present": 0,
        "hammer_present": 0,
        "shooting_star_present": 0,
        "spinning_top_present": 0,

        "bullish_engulfing_present": 0,
        "bearish_engulfing_present": 0,

        "morning_star_present": 0,
        "evening_star_present": 0,

        "three_white_soldiers_present": 0,
        "three_black_crows_present": 0,
    }

    for pattern in patterns:

        pattern_name = (
            pattern["pattern"]
            .lower()
            .replace(" ", "_")
        )

        feature_key = (
            f"{pattern_name}_present"
        )

        if feature_key in features:
            features[feature_key] = 1

        signal = str(
            pattern["signal"]
        ).lower()

        if "bullish" in signal:
            features[
                "bullish_pattern_present"
            ] = 1

        elif "bearish" in signal:
            features[
                "bearish_pattern_present"
            ] = 1

        else:
            features[
                "neutral_pattern_present"
            ] = 1

        features[
            "pattern_strength"
        ] += pattern.get(
            "strength",
            0,
        )

    return features