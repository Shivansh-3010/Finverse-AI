from services.prediction_dashboard_service import (
    PredictionDashboardService,
)


def test():

    result = (
        PredictionDashboardService.dashboard(
            symbol="RELIANCE",
        )
    )

    print(result)


if __name__ == "__main__":
    test()