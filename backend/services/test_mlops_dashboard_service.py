import pandas as pd

from services.mlops_dashboard_service import (
    MLOpsDashboardService,
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
        4.9,
        5.2,
    ]

    result = (
        MLOpsDashboardService.dashboard(
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

    assert "summary" in result
    assert "dashboard" in result
    assert "alerts" in result
    assert "selected_model" in result


if __name__ == "__main__":
    test()