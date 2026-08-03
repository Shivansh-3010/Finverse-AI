from forecasting.explainability_engine import (
    ExplainabilityEngine,
)


def test():

    comparison = {

        "xgboost": {
            "direction": "bullish",
            "predicted_return_pct": 1.25,
        },

        "prophet": {
            "direction": "bearish",
            "predicted_return_pct": -2.15,
        },

        "lstm": {
            "direction": "bullish",
            "predicted_return_pct": 0.42,
        },

        "transformer": {
            "direction": "bullish",
            "predicted_return_pct": 0.37,
        },
    }

    ensemble = {

        "direction": "bullish",

        "confidence": 82.6,

        "agreement_score": 79.4,

        "models_used": [
            "xgboost",
            "prophet",
            "lstm",
            "transformer",
        ],

        "model_predictions": {
            "xgboost": 1.25,
            "prophet": -2.15,
            "lstm": 0.42,
            "transformer": 0.37,
        },
    }

    result = (
        ExplainabilityEngine.explain(
            comparison=comparison,
            ensemble=ensemble,
        )
    )

    assert result["forecast"] == "BUY"
    assert "confidence" in result
    assert "reason" in result
    assert "model_predictions" in result

    print(result)


if __name__ == "__main__":
    test()