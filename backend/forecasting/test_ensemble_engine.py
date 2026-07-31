from forecasting.ensemble_engine import (
    EnsembleEngine,
)


def test():

    predictions = {
        "xgboost": 1.608,
        "prophet": 12.34,
        "lstm": 0.82,
        "transformer": 0.76,
    }

    comparison = {
        "xgboost": {
            "confidence": 92,
        },
        "prophet": {
            "confidence": 70,
        },
        "lstm": {
            "confidence": 86,
        },
        "transformer": {
            "confidence": 88,
        },
    }

    result = EnsembleEngine.combine(
        predictions=predictions,
        comparison=comparison,
    )

    print(result)

    assert "ensemble_return_pct" in result
    assert "confidence" in result
    assert "direction" in result
    assert len(result["models_used"]) == 4


if __name__ == "__main__":
    test()