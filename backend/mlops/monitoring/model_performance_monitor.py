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

        feature_drift = (
            FeatureDriftEngine.calculate(
                training_features,
                production_features,
            )
        )

        prediction_drift = (
            PredictionDriftEngine.calculate(
                historical_predictions,
                recent_predictions,
            )
        )

        return {

            "model": model_name,

            "symbol": symbol,

            "horizon": horizon,

            "registry": registry,

            "feature_drift": feature_drift,

            "prediction_drift": prediction_drift,

            "status": (

                "healthy"

                if not prediction_drift.get(
                    "drift_detected",
                    False,
                )

                else "warning"

            ),
        }