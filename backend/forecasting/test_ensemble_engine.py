from forecasting.ensemble_engine import (
    EnsembleEngine,
)


def test():

    result = (
        EnsembleEngine.combine(
            xgb_prediction_pct=1.608,
            prophet_forecast_price=1425.79,
            current_price=1269.20,
        )
    )

    print(result)


if __name__ == "__main__":
    test()