import pandas as pd

from mlops.monitoring.feature_drift_engine import (
    FeatureDriftEngine,
)

from mlops.monitoring.prediction_drift_engine import (
    PredictionDriftEngine,
)

from mlops.monitoring.model_drift_engine import (
    ModelDriftEngine,
)

from mlops.monitoring.target_drift_engine import (
    TargetDriftEngine,
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
        historical_evaluations,
        recent_evaluations,
        historical_targets,
        recent_targets,
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

        # -------------------------
        # Feature Drift
        # -------------------------

        if feature_data_sufficient:

            feature_drift = (
                FeatureDriftEngine.calculate(
                    training_features,
                    production_features,
                )
            )

        else:

            feature_drift = {}

        # -------------------------
        # Prediction Drift
        # -------------------------

        if prediction_data_sufficient:

            prediction_drift = (
                PredictionDriftEngine.calculate(
                    historical_predictions,
                    recent_predictions,
                )
            )

        else:

            prediction_drift = {}

        # -------------------------
        # Model Drift
        # -------------------------

        model_drift = (
            ModelDriftEngine.calculate(
                historical_evaluations,
                recent_evaluations,
            )
        )

        # -------------------------
        # Target Drift
        # -------------------------

        target_drift = (
            TargetDriftEngine.calculate(
                historical_targets,
                recent_targets,
            )
        )

        # -------------------------
        # Data Sufficiency
        # -------------------------

        model_drift_data_sufficient = (
            model_drift.get(
                "status"
            )
            != "insufficient_data"
        )

        target_drift_data_sufficient = (
            bool(target_drift)
        )

        all_data_sufficient = (
            feature_data_sufficient
            and prediction_data_sufficient
            and model_drift_data_sufficient
            and target_drift_data_sufficient
        )

        # -------------------------
        # Overall Status
        # -------------------------

        feature_drift_detected = any(
            item.get(
                "drift_detected",
                False,
            )
            for item in feature_drift.values()
        )

        prediction_drift_detected = (
            prediction_drift.get(
                "drift_detected",
                False,
            )
        )

        model_drift_detected = (
            model_drift.get(
                "drift_detected",
                False,
            )
        )

        target_drift_detected = (
            target_drift.get(
                "drift_detected",
                False,
            )
        )

        if not all_data_sufficient:

            status = "insufficient_data"

        elif (
            feature_drift_detected
            or prediction_drift_detected
            or model_drift_detected
            or target_drift_detected
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

            "model_drift": model_drift,

            "target_drift": target_drift,

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

                "historical_evaluation_rows":
                    len(historical_evaluations),

                "recent_evaluation_rows":
                    len(recent_evaluations),

                "model_drift_data_sufficient":
                    model_drift_data_sufficient,

                "target_drift_data_sufficient":
                    target_drift_data_sufficient,

                "feature_data_sufficient":
                    feature_data_sufficient,

                "prediction_data_sufficient":
                    prediction_data_sufficient,

                "all_data_sufficient":
                    all_data_sufficient,
            },
        }