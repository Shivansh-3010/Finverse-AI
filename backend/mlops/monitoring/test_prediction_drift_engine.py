from mlops.monitoring.prediction_drift_engine import (
    PredictionDriftEngine,
)


def test():

    historical = [
        0.8,
        1.0,
        0.9,
        1.2,
        1.1,
    ]

    recent = [
        4.8,
        5.1,
        5.0,
        4.9,
        5.2,
    ]

    result = (
        PredictionDriftEngine.calculate(
            historical,
            recent,
        )
    )

    print(result)

    assert (
        result["drift_detected"]
        is True
    )


if __name__ == "__main__":
    test()