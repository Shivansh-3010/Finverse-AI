import pandas as pd

from services.model_health_dashboard_service import (
    ModelHealthDashboardService,
)

from mlops.monitoring.model_performance_monitor import (
    ModelPerformanceMonitor,
)

from mlops.monitoring.drift_alert_engine import (
    DriftAlertEngine,
)


class MLOpsDashboardService:

    @staticmethod
    def dashboard(
        model_name: str,
        symbol: str,
        horizon: str,
        training_features: pd.DataFrame,
        production_features: pd.DataFrame,
        historical_predictions,
        recent_predictions,
    ):

        dashboard = (
            ModelHealthDashboardService.dashboard(
                training_features=training_features,
                production_features=production_features,
                historical_predictions=historical_predictions,
                recent_predictions=recent_predictions,
            )
        )

        report = (
            ModelPerformanceMonitor.monitor(
                model_name=model_name,
                symbol=symbol,
                horizon=horizon,
                training_features=training_features,
                production_features=production_features,
                historical_predictions=historical_predictions,
                recent_predictions=recent_predictions,
            )
        )

        alerts = (
            DriftAlertEngine.generate(
                report
            )
        )

        return {

            "summary": {

                "total_models":
                    dashboard["total_models"],

                "healthy_models":
                    dashboard["healthy_models"],

                "warning_models":
                    dashboard["warning_models"],

            },

            "dashboard": dashboard,

            "alerts": alerts,

            "selected_model": report,
        }