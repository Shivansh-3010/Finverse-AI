from database.session import SessionLocal

from services.historical_ohlcv_import_service import (
    HistoricalOHLCVImportService,
)

db = SessionLocal()

try:

    result = (
        HistoricalOHLCVImportService.import_csv(
            db=db,

            csv_path=
            r"C:\Projects\Finverse-AI\datasets\OHLCV\NIFTY-50 Stock Market Data (2000 - 2021)\RELIANCE.csv",

            limit=100,
        )
    )

    print(result)

finally:

    db.close()