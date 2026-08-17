import pandas as pd

from types import SimpleNamespace

from mlops.monitoring.model_performance_monitor import (
    ModelPerformanceMonitor,
)

from mlops.monitoring.drift_alert_engine import (
    DriftAlertEngine,
)


def make_evaluations(
    predicted,
    actual,
    count=10,
):

    evaluations = []

    for _ in range(count):

        evaluations.append(
            SimpleNamespace(
                predicted_return=predicted,
                actual_return=actual,
                absolute_error=abs(
                    predicted - actual
                ),
                directional_correct=float(
                    (
                        predicted >= 0
                        and actual >= 0
                    )
                    or (
                        predicted < 0
                        and actual < 0
                    )
                ),
            )
        )

    return evaluations


def test():

    training = pd.DataFrame({

        "rsi": [
            45,
            50,
            55,
        ],

        "macd": [
            0.2,
            0.3,
            0.4,
        ],

    })

    production = pd.DataFrame({

        "rsi": [
            70,
            71,
            69,
        ],

        "macd": [
            0.2,
            0.3,
            0.4,
        ],

    })

    historical_evaluations = (
        make_evaluations(
            predicted=1.0,
            actual=1.0,
            count=10,
        )
    )

    recent_evaluations = (
        make_evaluations(
            predicted=5.0,
            actual=1.0,
            count=10,
        )
    )

    report = (
        ModelPerformanceMonitor.monitor(
            model_name="xgboost",
            symbol="RELIANCE",
            horizon="5d",

            training_features=training,

            production_features=production,

            historical_predictions=[
                1.0,
                1.2,
                1.1,
            ],

            recent_predictions=[
                5.0,
                5.1,
                4.9,
            ],

            historical_evaluations=
                historical_evaluations,

            recent_evaluations=
                recent_evaluations,

            historical_targets=[
                0.8,
                1.0,
                1.1,
                0.9,
                1.0,
                0.9,
                1.1,
                1.0,
                0.8,
                1.0,
            ],

            recent_targets=[
                4.8,
                5.0,
                5.2,
                4.9,
                5.1,
                5.0,
                4.8,
                5.2,
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

    alert_types = {
        alert["type"]
        for alert in alerts
    }

    assert (
        "Model Drift"
        in alert_types
    )

    assert (
        "Target Drift"
        in alert_types
    )

    assert (
        "Recommendation"
        in alert_types
    )


if __name__ == "__main__":
    test()