from datetime import datetime

from database.session import SessionLocal
from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from data.ingestion.yahoo_ingestor import (
    YahooIngestor,
)

from constants.timeframes import (
    SUPPORTED_TIMEFRAMES,
)

class MultiTimeframeIngestionService:
    
    TIMEFRAME_CONFIG = {
        "1m": {
            "period": "7d",
            "interval": "1m",
        },
        "5m": {
            "period": "60d",
            "interval": "5m",
        },
        "15m": {
            "period": "60d",
            "interval": "15m",
        },
        "1h": {
            "period": "730d",
            "interval": "1h",
        },
        "4h": {
            "period": "730d",
            "interval": "1h",
        },
        "1d": {
            "period": "5y",
            "interval": "1d",
        },
        "1w": {
            "period": "10y",
            "interval": "1wk",
        },
        "1mo": {
            "period": "max",
            "interval": "1mo",
        },
    }

    def __init__(self):

        self.ingestor = YahooIngestor()
        
    def ingest_symbol(
        self,
        symbol: str
    ):

        db = SessionLocal()

        try:

            repository = OHLCVRepository(db)

            total_records = 0

            for timeframe in SUPPORTED_TIMEFRAMES:

                config = (
                    self.TIMEFRAME_CONFIG[
                        timeframe
                    ]
                )

                print(
                    f"Ingesting {symbol} "
                    f"[{timeframe}]..."
                )

                df = (
                    self.ingestor
                    .get_historical_data(
                        symbol=symbol,
                        period=config["period"],
                        interval=config["interval"],
                    )
                )

                if df.empty:
                    continue

                total_records += len(df)

            return {
                "symbol": symbol,
                "records": total_records,
            }

        finally:
            db.close()
            
            