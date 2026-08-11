import pandas as pd

from mlops.monitoring.feature_drift_engine import (
    FeatureDriftEngine,
)

from mlops.monitoring.prediction_drift_engine import (
    PredictionDriftEngine,
)

from mlops.registry.model_registry import (
    ModelRegistry,
)


class ModelPerformanceMonitor:

    MIN_FEATURE_PRODUCTION_ROWS = 10
    MIN_RECENT_PREDICTIONS = 10

    @staticmethod
    def monitor(
        model_name: str,
        symbol: str,
        horizon: str,
        training_features: pd.DataFrame,
        production_features: pd.DataFrame,
        historical_predictions,
        recent_predictions,
    ):

        registry = (
            ModelRegistry.get(
                model_name=model_name,
                symbol=symbol,
                horizon=horizon,
            )
        )

        feature_data_sufficient = (
            len(production_features)
            >= ModelPerformanceMonitor
            .MIN_FEATURE_PRODUCTION_ROWS
        )

        prediction_data_sufficient = (
            len(recent_predictions)
            >= ModelPerformanceMonitor
            .MIN_RECENT_PREDICTIONS
        )

        if feature_data_sufficient:

            feature_drift = (
                FeatureDriftEngine.calculate(
                    training_features,
                    production_features,
                )
            )

        else:

            feature_drift = {}

        if prediction_data_sufficient:

            prediction_drift = (
                PredictionDriftEngine.calculate(
                    historical_predictions,
                    recent_predictions,
                )
            )

        else:

            prediction_drift = {}

        if (
            not feature_data_sufficient
            or not prediction_data_sufficient
        ):

            status = "insufficient_data"

        elif (
            any(
                item["drift_detected"]
                for item in feature_drift.values()
            )
            or prediction_drift.get(
                "drift_detected",
                False,
            )
        ):

            status = "warning"

        else:

            status = "healthy"

        return {

            "model": model_name,

            "symbol": symbol,

            "horizon": horizon,

            "registry": registry,

            "feature_drift": feature_drift,

            "prediction_drift": prediction_drift,

            "status": status,

            "data_quality": {

                "feature_production_rows":
                    len(production_features),

                "required_feature_rows":
                    ModelPerformanceMonitor
                    .MIN_FEATURE_PRODUCTION_ROWS,

                "recent_prediction_rows":
                    len(recent_predictions),

                "required_prediction_rows":
                    ModelPerformanceMonitor
                    .MIN_RECENT_PREDICTIONS,

                "feature_data_sufficient":
                    feature_data_sufficient,

                "prediction_data_sufficient":
                    prediction_data_sufficient,

            },
        }