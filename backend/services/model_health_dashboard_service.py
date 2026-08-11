from mlops.monitoring.model_performance_monitor import (
    ModelPerformanceMonitor,
)

from mlops.registry.model_registry import (
    ModelRegistry,
)

from services.monitoring_data_service import (
    MonitoringDataService,
)


class ModelHealthDashboardService:

    MODELS = [
        ("xgboost", "RELIANCE", "1d", "5d"),
        ("prophet", "RELIANCE", "1d", "1d"),
        ("lstm", "RELIANCE", "1d", "1d"),
        ("transformer", "RELIANCE", "1d", "1d"),
    ]

    @staticmethod
    def dashboard():

        dashboard = []

        for (
            model_name,
            symbol,
            timeframe,
            horizon,
        ) in ModelHealthDashboardService.MODELS:

            registry = ModelRegistry.get(
                model_name=model_name,
                symbol=symbol,
                horizon=horizon,
            )

            if not registry:
                continue

            try:

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
                    )
                )

                feature_drift = report[
                    "feature_drift"
                ]

                dashboard.append({

                    "model": model_name,

                    "version":
                        registry["version"],

                    "status":
                        report["status"],

                    "training_date":
                        registry["training_date"],

                    "metrics":
                        registry["metrics"],

                    "feature_drift":
                        any(
                            item[
                                "drift_detected"
                            ]
                            for item in feature_drift.values()
                        ),

                    "prediction_drift":
                        report[
                            "prediction_drift"
                        ].get(
                            "drift_detected",
                            False,
                        ),

                    "data_quality":
                        report[
                            "data_quality"
                        ],

                })

            except Exception as exc:

                dashboard.append({

                    "model": model_name,

                    "version":
                        registry.get(
                            "version"
                        ),

                    "status": "error",

                    "training_date":
                        registry.get(
                            "training_date"
                        ),

                    "metrics":
                        registry.get(
                            "metrics",
                            {},
                        ),

                    "feature_drift":
                        False,

                    "prediction_drift":
                        False,

                    "data_quality": {},

                    "error": str(exc),

                })

        return {

            "total_models":
                len(dashboard),

            "healthy_models":
                sum(
                    1
                    for model in dashboard
                    if model["status"]
                    == "healthy"
                ),

            "warning_models":
                sum(
                    1
                    for model in dashboard
                    if model["status"]
                    == "warning"
                ),

            "insufficient_data_models":
                sum(
                    1
                    for model in dashboard
                    if model["status"]
                    == "insufficient_data"
                ),

            "error_models":
                sum(
                    1
                    for model in dashboard
                    if model["status"]
                    == "error"
                ),

            "models":
                dashboard,
        }