import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(
        str(PROJECT_ROOT)
    )
from apscheduler.schedulers.background import (
    BackgroundScheduler,
)

from data.ingestion.multi_timeframe_ingestor import (
    MultiTimeframeIngestor,
)
from constants.symbols import SYMBOLS
from database.session import SessionLocal

from services.historical_indicator_backfill_service import (
    HistoricalIndicatorBackfillService,
)

from services.historical_candlestick_backfill_service import (
    HistoricalCandlestickBackfillService,
)


scheduler = BackgroundScheduler()


def ingest_market_data():

    print(
        "Running scheduled ingestion..."
    )

    ingestor = MultiTimeframeIngestor()

    for symbol in SYMBOLS:

        print(
            f"Ingesting {symbol}"
        )

        inserted_rows = (
            ingestor.ingest_and_store(
                symbol
            )
        )

        print(
            f"{symbol}: "
            f"{inserted_rows} new rows"
        )

        if inserted_rows <= 0:
            continue

        clean_symbol = (
            symbol.replace(
                ".NS",
                ""
            )
        )

        db = SessionLocal()

        try:

            print(
                f"Updating indicators for "
                f"{clean_symbol}"
            )

            indicator_result = (
                HistoricalIndicatorBackfillService
                .backfill_symbol(
                    db=db,
                    symbol=clean_symbol,
                    timeframe="1d",
                )
            )

            print(
                "Indicators:",
                indicator_result
            )

            print(
                f"Updating candlestick patterns for "
                f"{clean_symbol}"
            )

            pattern_result = (
                HistoricalCandlestickBackfillService
                .backfill_symbol(
                    db=db,
                    symbol=clean_symbol,
                    timeframe="1d",
                )
            )

            print(
                "Patterns:",
                pattern_result
            )

        finally:

            db.close()


def start_scheduler():

    scheduler.add_job(
        ingest_market_data,
        trigger="interval",
        minutes=60,
        id="market_data_ingestion",
        replace_existing=True,
    )

    scheduler.start()


def stop_scheduler():

    scheduler.shutdown()