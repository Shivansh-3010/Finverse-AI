from services.model_health_dashboard_service import (
    ModelHealthDashboardService,
)

from services.monitoring_data_service import (
    MonitoringDataService,
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
        model_name: str = "xgboost",
        symbol: str = "RELIANCE",
        timeframe: str = "1d",
        horizon: str = "5d",
    ):

        dashboard = (
            ModelHealthDashboardService.dashboard()
        )

        data = (
            MonitoringDataService
            .get_model_data(
                model_name=model_name,
                symbol=symbol,
                timeframe=timeframe,
                horizon=horizon,
            )
        )

        report = (
            ModelPerformanceMonitor.monitor(
                model_name=model_name,
                symbol=symbol,
                horizon=horizon,

                training_features=data[
                    "training_features"
                ],

                production_features=data[
                    "production_features"
                ],

                historical_predictions=data[
                    "historical_predictions"
                ],

                recent_predictions=data[
                    "recent_predictions"
                ],

                historical_evaluations=data[
                    "historical_evaluations"
                ],

                recent_evaluations=data[
                    "recent_evaluations"
                ],

                historical_targets=data[
                    "historical_targets"
                ],

                recent_targets=data[
                    "recent_targets"
                ],
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
                    dashboard[
                        "total_models"
                    ],

                "healthy_models":
                    dashboard[
                        "healthy_models"
                    ],

                "warning_models":
                    dashboard[
                        "warning_models"
                    ],

                "insufficient_data_models":
                    dashboard[
                        "insufficient_data_models"
                    ],

                "error_models":
                    dashboard[
                        "error_models"
                    ],

            },

            "dashboard":
                dashboard,

            "alerts":
                alerts,

            "selected_model":
                report,
        }