import pandas as pd

from mlops.monitoring.model_performance_monitor import (
    ModelPerformanceMonitor,
)

from mlops.monitoring.drift_alert_engine import (
    DriftAlertEngine,
)


def test():

    training = pd.DataFrame({

        "rsi": [45, 50, 55],

        "macd": [0.2, 0.3, 0.4],

    })

    production = pd.DataFrame({

        "rsi": [70, 71, 69],

        "macd": [0.2, 0.3, 0.4],

    })

    report = (
        ModelPerformanceMonitor.monitor(
            model_name="xgboost",
            symbol="RELIANCE",
            horizon="5d",
            training_features=training,
            production_features=production,
            historical_predictions=[
                1,
                1.2,
                1.1,
            ],
            recent_predictions=[
                5,
                5.1,
                4.9,
            ],
        )
    )

    alerts = (
        DriftAlertEngine.generate(
            report,
        )
    )

    print(alerts)

    assert len(alerts) > 0


if __name__ == "__main__":
    test()