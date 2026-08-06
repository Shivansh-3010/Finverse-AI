from mlops.monitoring.retraining_recommendation_engine import (
    RetrainingRecommendationEngine,
)


def test():

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

    }

    result = (
        RetrainingRecommendationEngine.recommend(
            report
        )
    )

    print(result)

    assert result["recommend"] is True

    assert result["priority"] == "CRITICAL"

    assert len(result["reasons"]) == 3


if __name__ == "__main__":
    test()