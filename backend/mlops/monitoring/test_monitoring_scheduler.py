import pandas as pd

from mlops.monitoring.monitoring_scheduler import (
    MonitoringScheduler,
)


def test():

    training = pd.DataFrame({

        "rsi": [45, 50, 55],

        "macd": [0.2, 0.3, 0.4],

    })

    production = pd.DataFrame({

        "rsi": [70, 72, 69],

        "macd": [0.2, 0.3, 0.4],

    })

    historical = [

        1.0,

        1.1,

        0.9,

    ]

    recent = [

        5.0,

        5.2,

        4.9,

    ]

    result = (
        MonitoringScheduler.run(
            model_name="xgboost",
            symbol="RELIANCE",
            horizon="5d",
            training_features=training,
            production_features=production,
            historical_predictions=historical,
            recent_predictions=recent,
        )
    )

    print(result)

    assert result["completed"] is True

    assert "report" in result

    assert "alerts" in result

    assert "recommendation" in result


if __name__ == "__main__":
    test()