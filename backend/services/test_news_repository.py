from database.session import SessionLocal
from repositories.news_article_repository import (
    NewsArticleRepository,
)

db = SessionLocal()

try:

    repository = (
        NewsArticleRepository(db)
    )

    history = (
        repository.get_history(
            "AAPL"
        )
    )

    print(
        f"Articles: {len(history)}"
    )

    if history:

        print(
            history[-1].news_score
        )

finally:
    db.close()