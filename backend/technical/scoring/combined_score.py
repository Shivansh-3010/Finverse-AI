def calculate_combined_score(
    technical_score: float,
    candlestick_score: float,
) -> int:
    """
    Combine technical and candlestick scores.
    """

    return round(
        (technical_score + candlestick_score) / 2
    )