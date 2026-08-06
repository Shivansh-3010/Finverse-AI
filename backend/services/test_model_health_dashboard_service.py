import pandas as pd

from services.model_health_dashboard_service import (
    ModelHealthDashboardService,
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
        ModelHealthDashboardService.dashboard(
            training_features=training,
            production_features=production,
            historical_predictions=historical,
            recent_predictions=recent,
        )
    )

    print(result)

    assert "models" in result

    assert result["total_models"] >= 1


if __name__ == "__main__":
    test()