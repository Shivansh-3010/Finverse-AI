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
        
    def get_latest_by_symbol_and_timeframe(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 200
    ):
        return (
            self.db.query(OHLCVData)
            .filter(
                OHLCVData.symbol == symbol,
                OHLCVData.timeframe == timeframe
            )
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
        
    def get_history_by_symbol_and_timeframe(
        self,
        symbol: str,
        timeframe: str
    ):
        return (
            self.db.query(OHLCVData)
            .filter(
                OHLCVData.symbol == symbol,
                OHLCVData.timeframe == timeframe
            )
            .order_by(OHLCVData.timestamp)
            .all()
        )
        
    def get_latest_candle(
        self,
        symbol: str,
        timeframe: str
    ):
        return (
            self.db.query(OHLCVData)
            .filter(
                OHLCVData.symbol == symbol,
                OHLCVData.timeframe == timeframe
            )
            .order_by(
                desc(
                    OHLCVData.timestamp
                )
            )
            .first()
        )
        
    def exists(
        self,
        symbol: str,
        timeframe: str,
        timestamp,
    ):
        return (
            self.db.query(OHLCVData)
            .filter(
                OHLCVData.symbol == symbol,
                OHLCVData.timeframe == timeframe,
                OHLCVData.timestamp == timestamp,
            )
            .first()
            is not None
        )
        
    def get_existing_timestamps(
        self,
        symbol: str,
        timeframe: str,
    ):

        rows = (
            self.db.query(
                OHLCVData.timestamp
            )
            .filter(
                OHLCVData.symbol == symbol,
                OHLCVData.timeframe == timeframe,
            )
            .all()
        )

        return {
            row[0]
            for row in rows
        }
        
    def update_corporate_actions(
        self,
        symbol: str,
        timeframe: str,
        timestamp,
        dividend: float,
        stock_split: float,
    ):

        candle = (
            self.db.query(OHLCVData)
            .filter(
                OHLCVData.symbol == symbol,
                OHLCVData.timeframe == timeframe,
                OHLCVData.timestamp == timestamp,
            )
            .first()
        )

        if not candle:
            return False

        candle.dividend = dividend
        candle.stock_split = stock_split

        self.db.commit()

        return True
    
    def get_all_symbols(
        self,
        timeframe: str = "1d",
    ):
        rows = (
            self.db.query(
                OHLCVData.symbol
            )
            .filter(
                OHLCVData.timeframe == timeframe
            )
            .distinct()
            .all()
        )

        return [
            row[0]
            for row in rows
        ]
        
    def get_history_by_symbol_and_timeframe_between(
        self,
        symbol: str,
        timeframe: str,
        start_timestamp=None,
        end_timestamp=None,
    ):
        query = (
            self.db.query(
                OHLCVData
            )
            .filter(
                OHLCVData.symbol == symbol,
                OHLCVData.timeframe == timeframe,
            )
        )

        if start_timestamp is not None:
            query = query.filter(
                OHLCVData.timestamp >= start_timestamp
            )

        if end_timestamp is not None:
            query = query.filter(
                OHLCVData.timestamp <= end_timestamp
            )

        return (
            query
            .order_by(
                OHLCVData.timestamp
            )
            .all()
        )
