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
            
            PredictionPersistenceService.save_prediction(
                symbol=symbol,
                timeframe=timeframe,
                prediction_value=prediction,
                confidence=56.67,
                model_name="xgboost",
                horizon="1d",
            )

            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "predicted_return_pct": round(
                    prediction,
                    4
                ),
                "direction": (
                    "bullish"
                    if prediction > 0
                    else "bearish"
                ),
            }

        finally:
            db.close()