from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.risk_metric import RiskMetric


class RiskMetricRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def save(
        self,
        risk_metric: RiskMetric
    ):

        saved_metric = self.db.merge(
            risk_metric
        )

        self.db.commit()

        self.db.refresh(
            saved_metric
        )

        return saved_metric

    def get_latest(
        self,
        symbol: str,
        timeframe: str = "1d"
    ):

        return (
            self.db.query(
                RiskMetric
            )
            .filter(
                RiskMetric.symbol == symbol,
                RiskMetric.timeframe == timeframe
            )
            .order_by(
                desc(
                    RiskMetric.timestamp
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
                RiskMetric
            )
            .filter(
                RiskMetric.symbol == symbol,
                RiskMetric.timeframe == timeframe
            )
            .order_by(
                RiskMetric.timestamp
            )
            .all()
        )