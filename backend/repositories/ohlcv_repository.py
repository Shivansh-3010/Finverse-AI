from sqlalchemy.orm import Session

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