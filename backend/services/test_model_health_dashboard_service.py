from services.model_health_dashboard_service import (
    ModelHealthDashboardService,
)


def test():

    result = (
        ModelHealthDashboardService.dashboard()
    )

    print(result)

    assert "total_models" in result
    assert "models" in result
    assert "insufficient_data_models" in result