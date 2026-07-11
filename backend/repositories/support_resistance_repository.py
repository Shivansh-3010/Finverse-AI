from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.support_resistance import (
    SupportResistance,
)


class SupportResistanceRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_latest_by_timeframe(
        self,
        symbol: str,
        timeframe: str,
    ):
        return (
            self.db.query(
                SupportResistance
            )
            .filter(
                SupportResistance.symbol == symbol,
                SupportResistance.timeframe == timeframe,
            )
            .order_by(
                desc(
                    SupportResistance.timestamp
                )
            )
            .first()
        )

    def get_history_by_timeframe(
        self,
        symbol: str,
        timeframe: str,
    ):
        return (
            self.db.query(
                SupportResistance
            )
            .filter(
                SupportResistance.symbol == symbol,
                SupportResistance.timeframe == timeframe,
            )
            .order_by(
                SupportResistance.timestamp
            )
            .all()
        )

    def save(
        self,
        support_resistance: SupportResistance,
    ):
        saved_record = self.db.merge(
            support_resistance
        )

        self.db.commit()
        self.db.refresh(saved_record)

        return saved_record
    
    def bulk_insert(
        self,
        records: list,
    ):

        self.db.bulk_save_objects(
            records
        )

        self.db.commit()