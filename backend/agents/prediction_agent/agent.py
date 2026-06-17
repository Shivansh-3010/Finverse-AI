from typing import Dict

import pandas as pd

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


class PredictionAgent:

    @staticmethod
    def predict(
        symbol: str,
        timeframe: str = "1d"
    ) -> Dict:

        db = SessionLocal()

        try:

            features = FeatureBuilder.build(
                db=db,
                symbol=symbol,
                timeframe=timeframe
            )

            feature_names = (
                ModelLoader.load_features()
            )

            model = (
                ModelLoader.load_model()
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
                horizon="1d",
            )

            ensemble = (
                EnsembleForecastService.forecast(
                    db=db,
                    symbol=symbol,
                    timeframe=timeframe,
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

            return {
                "symbol": symbol,
                "timeframe": timeframe,

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