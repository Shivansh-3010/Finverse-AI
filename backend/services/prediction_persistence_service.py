from datetime import datetime, timezone

from database.session import SessionLocal

from models.prediction import Prediction

from repositories.prediction_repository import (
    PredictionRepository,
)


class PredictionPersistenceService:

    @staticmethod
    def save_prediction(
        symbol: str,
        timeframe: str,
        prediction_value: float,
        confidence: float,
        model_name: str = "xgboost",
        horizon: str = "1d",
    ):

        db = SessionLocal()

        try:

            entity = Prediction(
                symbol=symbol,
                timeframe=timeframe,
                timestamp=datetime.now(
                    timezone.utc
                ),
                model_name=model_name,
                prediction=prediction_value,
                confidence=confidence,
                horizon=horizon,
            )

            return (
                PredictionRepository(db)
                .save(entity)
            )

        finally:
            db.close()