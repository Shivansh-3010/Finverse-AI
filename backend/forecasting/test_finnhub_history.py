import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))
from data.ingestion.news.finnhub_ingestor import (
    FinnhubIngestor,
)


def test():

    api = FinnhubIngestor()

    news = api.get_company_news(
        symbol="RELIANCE",
        from_date="2026-05-01",
        to_date="2026-06-16",
    )

    print(
        "Articles:",
        len(news)
    )

    if news:
        print(news[0])

if __name__ == "__main__":
    test()