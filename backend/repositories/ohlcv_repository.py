from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.ohlcv_data import OHLCVData


class OHLCVRepository:

    def __init__(self, db: Session):
        self.db = db

    def bulk_insert(self, records: list[dict]):

        objects = [
            OHLCVData(**record)
            for record in records
        ]

        self.db.bulk_save_objects(objects)
        self.db.commit()
    
    def get_latest_by_symbol(
        self,
        symbol: str,
        limit: int = 200
    ):
        return (
            self.db.query(OHLCVData)
            .filter(OHLCVData.symbol == symbol)
            .order_by(desc(OHLCVData.timestamp))
            .limit(limit)
            .all()
        )

    def get_history_by_symbol(
        self,
        symbol: str
    ):
        return (
            self.db.query(OHLCVData)
            .filter(OHLCVData.symbol == symbol)
            .order_by(OHLCVData.timestamp)
            .all()
        )      
