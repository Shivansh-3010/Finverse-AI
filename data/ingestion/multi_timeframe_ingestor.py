import sys
from pathlib import Path
from sqlalchemy.dialects.postgresql import (
    insert,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT / "backend") not in sys.path:
    sys.path.append(
        str(PROJECT_ROOT / "backend")
    )

import pandas as pd

from database.session import SessionLocal
from models.ohlcv_data import OHLCVData

from data.ingestion.yahoo_ingestor import (
    YahooIngestor,
)


TIMEFRAME_CONFIG = {
    "1m": {"period": "7d", "interval": "1m"},
    "5m": {"period": "60d", "interval": "5m"},
    "15m": {"period": "60d", "interval": "15m"},
    "1h": {"period": "730d", "interval": "1h"},
    "1d": {"period": "5y", "interval": "1d"},
    "1w": {"period": "10y", "interval": "1wk"},
    "1mo": {"period": "max", "interval": "1mo"},
}


class MultiTimeframeIngestor:
    
    def create_4h_candles(
        self,
        df: pd.DataFrame
    ):

        if df.empty:
            return df

        four_hour = (
            df.resample("4h")
            .agg(
                {
                    "Open": "first",
                    "High": "max",
                    "Low": "min",
                    "Close": "last",
                    "Volume": "sum",
                }
            )
            .dropna()
        )

        return four_hour
    
    def fetch_all_timeframes(
        self,
        symbol: str
    ):

        results = {}

        for timeframe, config in TIMEFRAME_CONFIG.items():

            print(
                f"Fetching {symbol} [{timeframe}]..."
            )

            df = self.ingestor.get_historical_data(
                symbol=symbol,
                period=config["period"],
                interval=config["interval"],
            )

            results[timeframe] = df
            
            if timeframe == "1h":

                results["4h"] = (
                    self.create_4h_candles(df)
                )

        return results
    
    def save_dataframe(
        self,
        symbol: str,
        timeframe: str,
        df
    ):

        if df.empty:
            return 0

        db = SessionLocal()

        try:

            records = []

            clean_symbol = symbol.replace(
                ".NS",
                ""
            )

            for timestamp, row in df.iterrows():

                records.append(
                    {
                        "symbol": clean_symbol,
                        "timeframe": timeframe,
                        "timestamp": timestamp,
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        "volume": int(row["Volume"]),
                    }
                )

            stmt = (
                insert(OHLCVData)
                .values(records)
                .on_conflict_do_nothing(
                    index_elements=[
                        "symbol",
                        "timeframe",
                        "timestamp",
                    ]
                )
            )

            result = db.execute(stmt)

            db.commit()

            return result.rowcount

        finally:
            db.close()
            
    def ingest_and_store(
        self,
        symbol: str
    ):

        results = self.fetch_all_timeframes(
            symbol
        )

        total_rows = 0

        for timeframe, df in results.items():

            saved = self.save_dataframe(
                symbol=symbol,
                timeframe=timeframe,
                df=df,
            )

            print(
                f"{timeframe}: "
                f"{saved} rows"
            )

            total_rows += saved

        return total_rows

    def __init__(self):
        self.ingestor = YahooIngestor()