import pandas as pd

from mlops.monitoring.feature_drift_engine import (
    FeatureDriftEngine,
)


def test():

    training = pd.DataFrame({

        "rsi": [
            45,
            48,
            50,
            52,
            55,
        ],

        "macd": [
            0.2,
            0.3,
            0.4,
            0.5,
            0.4,
        ],
    })

    production = pd.DataFrame({

        "rsi": [
            62,
            65,
            66,
            64,
            67,
        ],

        "macd": [
            0.25,
            0.30,
            0.35,
            0.40,
            0.50,
        ],
    })

    result = (
        FeatureDriftEngine.calculate(
            training,
            production,
        )
    )

    print(result)

    assert "rsi" in result
    assert "macd" in result


if __name__ == "__main__":
    test()