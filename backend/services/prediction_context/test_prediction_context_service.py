from services.prediction_context.prediction_context_service import (
    PredictionContextService,
)


def test():

    result = (
        PredictionContextService.build(
            symbol="RELIANCE",
        )
    )

    print(result)

    assert "prediction" in result
    assert "feature_store" in result
    assert "comparison" in result
    assert "evaluation" in result
    assert "leaderboard" in result


if __name__ == "__main__":
    test()