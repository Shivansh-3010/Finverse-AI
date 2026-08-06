import pandas as pd

from mlops.monitoring.model_performance_monitor import (
    ModelPerformanceMonitor,
)

from mlops.registry.model_registry import (
    ModelRegistry,
)


class ModelHealthDashboardService:

    @staticmethod
    def dashboard(
        training_features: pd.DataFrame,
        production_features: pd.DataFrame,
        historical_predictions,
        recent_predictions,
    ):

        dashboard = []

        models = [

            ("xgboost", "RELIANCE", "5d"),

            ("prophet", "RELIANCE", "1d"),

            ("lstm", "RELIANCE", "1d"),

            ("transformer", "RELIANCE", "1d"),

        ]

        for (
            model_name,
            symbol,
            horizon,
        ) in models:

            registry = ModelRegistry.get(
                model_name=model_name,
                symbol=symbol,
                horizon=horizon,
            )

            if registry is None:
                continue

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

            dashboard.append({

                "model": model_name,

                "version": registry["version"],

                "status": report["status"],

                "training_date": registry["training_date"],

                "metrics": registry["metrics"],

                "feature_drift": any(
                    item["drift_detected"]
                    for item in report[
                        "feature_drift"
                    ].values()
                ),

                "prediction_drift":
                    report[
                        "prediction_drift"
                    ][
                        "drift_detected"
                    ],
            })

        return {

            "total_models": len(
                dashboard
            ),

            "healthy_models": sum(

                1

                for m in dashboard

                if m["status"] == "healthy"

            ),

            "warning_models": sum(

                1

                for m in dashboard

                if m["status"] == "warning"

            ),

            "models": dashboard,
        }