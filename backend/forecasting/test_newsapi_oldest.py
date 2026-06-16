import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from data.ingestion.news.newsapi_ingestor import (
    NewsAPIIngestor
)

newsapi = NewsAPIIngestor()

response = newsapi.get_company_news(
    query="Reliance Industries"
)

articles = response.get(
    "articles",
    []
)

print(
    "Articles:",
    len(articles)
)

if articles:

    print(
        "\nNewest:"
    )

    print(
        articles[0][
            "publishedAt"
        ]
    )

    print(
        "\nOldest:"
    )

    print(
        articles[-1][
            "publishedAt"
        ]
    )