import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]

if str(BACKEND_ROOT) not in sys.path:
    sys.path.append(str(BACKEND_ROOT))

from services.news_ingestion_service import (
    NewsIngestionService
)

symbols = [
    "HCLTECH",
    "WIPRO",
    "BDL",
    "AXISBANK",
    "KOTAKBANK",
    "BEL",
    "ONGC",
    "BPCL",
    "NTPC",
    "LT",
    "SUNPHARMA",
    "ITC",
    "ZOMATO",
    "IRB",
]

service = NewsIngestionService()

for symbol in symbols:

    try:

        result = service.ingest_news(
            symbol
        )

        print(
            f"{symbol}: "
            f"Fetched={result['fetched']} "
            f"Stored={result['stored']}"
        )

    except Exception as e:

        print(
            f"{symbol}: ERROR -> {e}"
        )