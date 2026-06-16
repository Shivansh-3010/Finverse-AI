from database.session import SessionLocal

from repositories.news_article_repository import (
    NewsArticleRepository,
)


def test_news_providers():

    db = SessionLocal()

    try:

        articles = (
            NewsArticleRepository(db)
            .get_history("RELIANCE")
        )

        print(
            "Total Articles:",
            len(articles)
        )

        for article in articles:

            print("-" * 50)

            print(
                "Provider:",
                article.provider
            )

            print(
                "Source:",
                article.source
            )

            print(
                "Published:",
                article.published_at
            )

            print(
                "Provider ID:",
                article.provider_article_id
            )

            print(
                "Title:",
                article.title
            )

    finally:
        db.close()


if __name__ == "__main__":
    test_news_providers()