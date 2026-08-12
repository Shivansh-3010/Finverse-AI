import pytest

from data.ingestion.news.newsapi_ingestor import (
    NewsAPIIngestor,
)


def test_newsapi_oldest():
    newsapi = NewsAPIIngestor()

    try:
        response = newsapi.get_company_news(
            query="Reliance Industries"
        )
    except Exception as exc:
        pytest.skip(
            f"NewsAPI unavailable during test: {exc}"
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