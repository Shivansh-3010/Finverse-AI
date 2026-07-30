from typing import Dict

import pandas as pd

import time

from metrics.monitoring_metrics import (
    MonitoringMetrics,
)

from database.session import SessionLocal

from forecasting.feature_builder import (
    FeatureBuilder,
)

from forecasting.model_loader import (
    ModelLoader,
)
from services.prediction_persistence_service import (
    PredictionPersistenceService,
)
from forecasting.confidence_engine import (
    ConfidenceEngine,
)

from repositories.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)

from forecasting.evaluation_metrics_engine import (
    EvaluationMetricsEngine,
)
from services.ensemble_forecast_service import (
    EnsembleForecastService,
)

from forecasting.explainability_engine import (
    ExplainabilityEngine,
)
from forecasting.horizons import (
    SUPPORTED_HORIZONS,
)

from repositories.prediction_repository import (
    PredictionRepository,
)

from forecasting.model_drift_engine import (
    ModelDriftEngine,
)


class PredictionAgent:

    @staticmethod
    def predict(
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
    ) -> Dict:

        db = SessionLocal()
        
        start_time = time.perf_counter()
        
        if horizon not in SUPPORTED_HORIZONS:

            raise ValueError(
                f"Unsupported horizon: {horizon}"
            )

        try:

            features = FeatureBuilder.build(
                db=db,
                symbol=symbol,
                timeframe=timeframe
            )

            feature_names = (
                ModelLoader.load_features(
                    model_type="xgboost",
                    horizon=horizon,
                )
            )

            model = (
                ModelLoader.load_model(
                    model_type="xgboost",
                    symbol=symbol,
                    horizon=horizon,
                )
            )
            X = pd.DataFrame(
                [features],
                columns=feature_names
            )

            prediction = float(
                model.predict(X)[0]
            )
            
            evaluations = (
                PredictionEvaluationRepository(db)
                .get_history(
                    symbol,
                    timeframe
                )
            )
            
            prediction_history = (
                PredictionRepository(db)
                .get_history(
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                )
            )

            MonitoringMetrics.prediction_model_drift = (
                ModelDriftEngine.calculate(
                    prediction_history
                )
            )

            if evaluations:

                confidence = (
                    ConfidenceEngine.calculate(
                        mae=
                            EvaluationMetricsEngine.mae(
                                evaluations
                            ),

                        directional_accuracy=
                            EvaluationMetricsEngine.directional_accuracy(
                                evaluations
                            ),
                    )
                )

            else:

                confidence = 50.0
            
            PredictionPersistenceService.save_prediction(
                symbol=symbol,
                timeframe=timeframe,
                prediction_value=prediction,
                confidence=confidence,
                model_name="xgboost",
                horizon=horizon,
            )

            ensemble = (
                EnsembleForecastService.forecast(
                    db=db,
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                )
            )

            explanation = (
                ExplainabilityEngine.explain(
                    direction=
                        ensemble["direction"],

                    confidence=
                        ensemble["confidence"],

                    xgb_return=
                        ensemble[
                            "xgboost_return_pct"
                        ],

                    prophet_return=
                        ensemble[
                            "prophet_return_pct"
                        ],
                )
            )
            
            latency_ms = (
                time.perf_counter() - start_time
            ) * 1000

            MonitoringMetrics.prediction_inference_latency_ms = (
                round(latency_ms, 2)
            )

            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "horizon": horizon,

                "forecast":
                    explanation["forecast"],

                "confidence":
                    explanation["confidence"],

                "predicted_return_pct":
                    ensemble[
                        "ensemble_return_pct"
                    ],

                "direction":
                    ensemble["direction"],

                "reason":
                    explanation["reason"],
            }

        finally:
            db.close()