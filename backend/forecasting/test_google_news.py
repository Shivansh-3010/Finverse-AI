import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(
        str(PROJECT_ROOT)
    )

from data.ingestion.news.google_news_ingestor import (
    GoogleNewsIngestor
)

api = GoogleNewsIngestor()

articles = (
    api.get_company_news(
        "Reliance Industries"
    )
)

print(
    "Articles:",
    len(articles)
)

if articles:
    print(
        articles[0]
    )