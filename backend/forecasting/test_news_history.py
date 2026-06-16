from database.session import SessionLocal

from repositories.news_article_repository import (
    NewsArticleRepository,
)


def test_news_history():

    db = SessionLocal()

    try:

        records = (
            NewsArticleRepository(db)
            .get_history(
                "RELIANCE"
            )
        )

        print(
            "News Count:",
            len(records)
        )

        if records:

            print(
                "First:",
                records[0].published_at
            )

            print(
                "Last:",
                records[-1].published_at
            )

            latest = records[-1]

            print(
                "Latest Score:",
                latest.news_score
            )

            print(
                "Latest Confidence:",
                latest.confidence
            )

    finally:
        db.close()


if __name__ == "__main__":
    test_news_history()