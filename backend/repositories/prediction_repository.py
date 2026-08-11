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
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        return (
            self.db.query(
                Prediction
            )
            .filter(
                Prediction.symbol == symbol,
                Prediction.timeframe == timeframe,
                Prediction.horizon == horizon,
            )
            .order_by(
                desc(
                    Prediction.timestamp
                )
            )
            .first()
        )

    def get_latest_predictions(
        self,
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        latest_timestamp = (
            self.db.query(
                Prediction.timestamp
            )
            .filter(
                Prediction.symbol == symbol,
                Prediction.timeframe == timeframe,
                Prediction.horizon == horizon,
            )
            .order_by(
                desc(Prediction.timestamp)
            )
            .limit(1)
            .scalar()
        )

        if latest_timestamp is None:
            return []

        return (
            self.db.query(
                Prediction
            )
            .filter(
                Prediction.symbol == symbol,
                Prediction.timeframe == timeframe,
                Prediction.horizon == horizon,
                Prediction.timestamp == latest_timestamp,
            )
            .all()
        )

    def get_history(
        self,
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        return (
            self.db.query(
                Prediction
            )
            .filter(
                Prediction.symbol == symbol,
                Prediction.timeframe == timeframe,
                Prediction.horizon == horizon,
            )
            .order_by(
                Prediction.timestamp
            )
            .all()
        )

    def get_history_by_model(
        self,
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
        model_name: str = "xgboost",
    ):

        return (
            self.db.query(
                Prediction
            )
            .filter(
                Prediction.symbol == symbol,
                Prediction.timeframe == timeframe,
                Prediction.horizon == horizon,
                Prediction.model_name == model_name,
            )
            .order_by(
                Prediction.timestamp
            )
            .all()
        )

    def get_recent_history_by_model(
        self,
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
        model_name: str = "xgboost",
        limit: int = 50,
    ):

        rows = (
            self.db.query(
                Prediction
            )
            .filter(
                Prediction.symbol == symbol,
                Prediction.timeframe == timeframe,
                Prediction.horizon == horizon,
                Prediction.model_name == model_name,
            )
            .order_by(
                desc(Prediction.timestamp)
            )
            .limit(limit)
            .all()
        )

        return list(
            reversed(rows)
        )