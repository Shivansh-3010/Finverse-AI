from forecasting.explainability_engine import (
    ExplainabilityEngine,
)


def test():

    result = (
        ExplainabilityEngine.explain(
            direction="bullish",
            confidence=88.4,
            xgb_return=1.608,
            prophet_return=7.8512,
        )
    )

    print(result)


if __name__ == "__main__":
    test()