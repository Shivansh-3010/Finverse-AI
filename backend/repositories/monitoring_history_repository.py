from sqlalchemy.orm import Session

from models.monitoring_history import (
    MonitoringHistory,
)


class MonitoringHistoryRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def save(
        self,
        entity: MonitoringHistory,
    ):

        self.db.add(entity)

        self.db.commit()

        self.db.refresh(entity)

        return entity

    def history(self):

        return (
            self.db.query(
                MonitoringHistory
            )
            .order_by(
                MonitoringHistory.timestamp.desc()
            )
            .all()
        )