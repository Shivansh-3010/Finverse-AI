from forecasting.adaptive_weight_engine import (
    AdaptiveWeightEngine,
)


def test():

    leaderboard = [
        {
            "model": "xgboost",
            "mae": 0.6,
            "directional_accuracy": 92,
        },
        {
            "model": "lstm",
            "mae": 0.8,
            "directional_accuracy": 88,
        },
        {
            "model": "transformer",
            "mae": 0.7,
            "directional_accuracy": 90,
        },
        {
            "model": "prophet",
            "mae": 1.4,
            "directional_accuracy": 70,
        },
    ]

    weights = (
        AdaptiveWeightEngine.calculate(
            leaderboard
        )
    )

    assert len(weights) == 4

    assert abs(
        sum(weights.values()) - 1
    ) < 1e-6

    print(weights)