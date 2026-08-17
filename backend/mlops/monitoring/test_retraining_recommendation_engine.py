from mlops.monitoring.retraining_recommendation_engine import (
    RetrainingRecommendationEngine,
)


def test_all_retraining_signals():

    report = {

        "registry": {

            "metrics": {

                "directional_accuracy": 52,

            }

        },

        "feature_drift": {

            "rsi": {

                "drift_detected": True,

            },

            "macd": {

                "drift_detected": False,

            },

        },

        "prediction_drift": {

            "drift_detected": True,

        },

        "model_drift": {

            "drift_detected": True,

            "severity": "HIGH",

        },

        "target_drift": {

            "drift_detected": True,

            "severity": "CRITICAL",

        },

    }

    result = (
        RetrainingRecommendationEngine.recommend(
            report
        )
    )

    print(result)

    assert (
        result["recommend"]
        is True
    )

    assert (
        result["priority"]
        == "CRITICAL"
    )

    assert (
        "Feature Drift"
        in result["reasons"]
    )

    assert (
        "Prediction Drift"
        in result["reasons"]
    )

    assert (
        "Model Drift"
        in result["reasons"]
    )

    assert (
        "Target Drift"
        in result["reasons"]
    )

    assert (
        "Low Directional Accuracy"
        in result["reasons"]
    )

    assert (
        len(result["reasons"])
        == 5
    )

    assert (
        result["recommended_action"]
        == "Retrain model"
    )


def test_no_retraining_required():

    report = {

        "registry": {

            "metrics": {

                "directional_accuracy": 70,

            }

        },

        "feature_drift": {},

        "prediction_drift": {

            "drift_detected": False,

        },

        "model_drift": {

            "drift_detected": False,

        },

        "target_drift": {

            "drift_detected": False,

        },

    }

    result = (
        RetrainingRecommendationEngine.recommend(
            report
        )
    )

    print(result)

    assert (
        result["recommend"]
        is False
    )

    assert (
        result["priority"]
        == "LOW"
    )

    assert (
        result["reasons"]
        == []
    )

    assert (
        result["recommended_action"]
        == "No action required"
    )


if __name__ == "__main__":
    test_all_retraining_signals()