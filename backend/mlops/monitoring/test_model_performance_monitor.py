import pandas as pd

from mlops.monitoring.model_performance_monitor import (
    ModelPerformanceMonitor,
)


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
            72,
            69,
        ],

        "macd": [
            0.2,
            0.3,
            0.4,
        ],
    })

    historical = [
        1.0,
        1.1,
        0.9,
    ]

    recent = [
        5.0,
        4.9,
        5.2,
    ]

    result = (
        ModelPerformanceMonitor.monitor(
            model_name="xgboost",
            symbol="RELIANCE",
            horizon="5d",

            training_features=training,
            production_features=production,

            historical_predictions=historical,
            recent_predictions=recent,

            historical_evaluations=[],
            recent_evaluations=[],

            historical_targets=[],
            recent_targets=[],
        )
    )

    print(result)

    # -------------------------
    # Basic Report Checks
    # -------------------------

    assert (
        result["model"]
        == "xgboost"
    )

    assert (
        result["symbol"]
        == "RELIANCE"
    )

    assert (
        result["horizon"]
        == "5d"
    )

    assert "registry" in result

    # -------------------------
    # Drift Reports
    # -------------------------

    assert (
        "feature_drift"
        in result
    )

    assert (
        "prediction_drift"
        in result
    )

    assert (
        "model_drift"
        in result
    )

    assert (
        "target_drift"
        in result
    )

    # -------------------------
    # Overall Status
    # -------------------------

    assert (
        result["status"]
        == "insufficient_data"
    )

    # -------------------------
    # Feature Data
    # -------------------------

    assert (
        result["data_quality"]
        ["feature_data_sufficient"]
        is False
    )

    # -------------------------
    # Prediction Data
    # -------------------------

    assert (
        result["data_quality"]
        ["prediction_data_sufficient"]
        is False
    )

    # -------------------------
    # Model Drift
    # -------------------------

    assert (
        result["model_drift"]
        ["status"]
        == "insufficient_data"
    )

    assert (
        result["model_drift"]
        ["drift_detected"]
        is False
    )

    assert (
        result["data_quality"]
        ["model_drift_data_sufficient"]
        is False
    )

    # -------------------------
    # Target Drift
    # -------------------------

    assert (
        result["target_drift"]
        == {}
    )

    assert (
        result["data_quality"]
        ["target_drift_data_sufficient"]
        is False
    )

    # -------------------------
    # Overall Data Quality
    # -------------------------

    assert (
        result["data_quality"]
        ["all_data_sufficient"]
        is False
    )


if __name__ == "__main__":
    test()