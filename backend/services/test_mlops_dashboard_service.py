from services.mlops_dashboard_service import (
    MLOpsDashboardService,
)


def test():

    result = (
        MLOpsDashboardService.dashboard(
            model_name="xgboost",
            symbol="RELIANCE",
            timeframe="1d",
            horizon="5d",
        )
    )

    print(result)

    assert "summary" in result

    assert "dashboard" in result

    assert "alerts" in result

    assert "selected_model" in result

    assert (
        result["summary"]["total_models"]
        == 4
    )

    assert (
        "insufficient_data_models"
        in result["summary"]
    )

    assert (
        result["selected_model"]["model"]
        == "xgboost"
    )

    assert (
        "data_quality"
        in result["selected_model"]
    )


if __name__ == "__main__":
    test()