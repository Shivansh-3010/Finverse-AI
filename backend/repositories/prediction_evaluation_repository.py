from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.prediction_evaluation import (
    PredictionEvaluation,
)


class PredictionEvaluationRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def save(
        self,
        evaluation: PredictionEvaluation
    ):

        saved_evaluation = (
            self.db.merge(
                evaluation
            )
        )

        self.db.commit()

        self.db.refresh(
            saved_evaluation
        )

        return saved_evaluation

    def get_latest(
        self,
        symbol: str,
        timeframe: str = "1d"
    ):

        return (
            self.db.query(
                PredictionEvaluation
            )
            .filter(
                PredictionEvaluation.symbol
                == symbol,

                PredictionEvaluation.timeframe
                == timeframe
            )
            .order_by(
                desc(
                    PredictionEvaluation.timestamp
                )
            )
            .first()
        )

    def get_history(
        self,
        symbol: str,
        timeframe: str = "1d"
    ):

        return (
            self.db.query(
                PredictionEvaluation
            )
            .filter(
                PredictionEvaluation.symbol
                == symbol,

                PredictionEvaluation.timeframe
                == timeframe
            )
            .order_by(
                PredictionEvaluation.timestamp
            )
            .all()
        )
        
    def get_recent_history(
        self,
        symbol: str,
        timeframe: str = "1d",
        limit: int = 50,
        model_name: str | None = None,
    ):

        query = (
            self.db.query(
                PredictionEvaluation
            )
            .filter(
                PredictionEvaluation.symbol
                == symbol,

                PredictionEvaluation.timeframe
                == timeframe,
            )
        )

        if model_name is not None:

            query = query.filter(
                PredictionEvaluation.model_name
                == model_name
            )

        evaluations = (
            query
            .order_by(
                desc(
                    PredictionEvaluation.timestamp
                )
            )
            .limit(limit)
            .all()
        )

        return list(
            reversed(evaluations)
        )