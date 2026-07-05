from database.session import SessionLocal

from repositories.news_article_repository import (
    NewsArticleRepository,
)


def test_news_distribution():

    db = SessionLocal()

    try:

        symbol = "RELIANCE"

        news = (
            NewsArticleRepository(db)
            .get_history(
                symbol=symbol
            )
        )

        print("\nTotal News Articles:")
        print(len(news))

        dates = {
            n.published_at.date()
            for n in news
            if n.published_at
        }

        print("\nUnique News Dates:")
        print(len(dates))

        sorted_dates = sorted(dates)

        print("\nFirst Date:")
        print(sorted_dates[0])

        print("\nLast Date:")
        print(sorted_dates[-1])

        assert True

    finally:
        db.close()