from forecasting.model_leaderboard_engine import (
    ModelLeaderboardEngine,
)


class DummyEvaluation:

    def __init__(
        self,
        actual,
        predicted,
    ):

        self.actual_return = actual
        self.predicted_return = predicted
        self.absolute_error = abs(
            predicted - actual
        )

        self.directional_correct = (
            (
                actual >= 0
                and predicted >= 0
            )
            or (
                actual < 0
                and predicted < 0
            )
        )


def build_history(
    prediction,
):

    return [
        DummyEvaluation(
            1.0,
            prediction,
        )
        for _ in range(50)
    ]


def test():

    leaderboard = (
        ModelLeaderboardEngine.rank(
            {
                "xgboost": build_history(
                    0.95
                ),
                "lstm": build_history(
                    0.90
                ),
                "transformer": build_history(
                    0.98
                ),
                "prophet": build_history(
                    0.70
                ),
            }
        )
    )

    assert len(
        leaderboard
    ) == 4

    assert (
        leaderboard[0]["rank"]
        == 1
    )

    print(
        leaderboard
    )