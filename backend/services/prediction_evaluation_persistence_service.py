from datetime import datetime

from database.session import SessionLocal

from models.prediction_evaluation import (
    PredictionEvaluation,
)

from repositories.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)


class PredictionEvaluationPersistenceService:

    @staticmethod
    def save_evaluation(
        symbol: str,
        timeframe: str,
        prediction_timestamp: datetime,
        horizon: str,
        model_name: str,
        predicted_return: float,
        actual_return: float,
    ):

        db = SessionLocal()

        try:

            absolute_error = abs(
                predicted_return
                - actual_return
            )

            directional_correct = float(
                (
                    predicted_return >= 0
                    and actual_return >= 0
                )
                or
                (
                    predicted_return < 0
                    and actual_return < 0
                )
            )

            entity = PredictionEvaluation(
                symbol=symbol,
                timeframe=timeframe,
                timestamp=prediction_timestamp,
                model_name=model_name,
                horizon=horizon,

                predicted_return=predicted_return,

                actual_return=actual_return,

                absolute_error=absolute_error,

                directional_correct=directional_correct,
            )

            return (
                PredictionEvaluationRepository(db)
                .save(entity)
            )

        finally:
            db.close()