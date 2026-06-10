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

        ingestor.ingest_and_store(
            symbol
        )


def start_scheduler():

    scheduler.add_job(
        ingest_market_data,
        trigger="interval",
        minutes=15,
        id="market_data_ingestion",
        replace_existing=True,
    )

    scheduler.start()


def stop_scheduler():

    scheduler.shutdown()