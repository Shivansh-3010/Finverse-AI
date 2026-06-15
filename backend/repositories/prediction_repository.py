from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.prediction import Prediction


class PredictionRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def save(
        self,
        prediction: Prediction
    ):

        saved_prediction = (
            self.db.merge(
                prediction
            )
        )

        self.db.commit()

        self.db.refresh(
            saved_prediction
        )

        return saved_prediction

    def get_latest(
        self,
        symbol: str,
        timeframe: str = "1d"
    ):

        return (
            self.db.query(
                Prediction
            )
            .filter(
                Prediction.symbol == symbol,
                Prediction.timeframe == timeframe
            )
            .order_by(
                desc(
                    Prediction.timestamp
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
                Prediction
            )
            .filter(
                Prediction.symbol == symbol,
                Prediction.timeframe == timeframe
            )
            .order_by(
                Prediction.timestamp
            )
            .all()
        )