from database.session import SessionLocal

from repositories.news_article_repository import (
    NewsArticleRepository,
)

from forecasting.news_feature_builder import (
    NewsFeatureBuilder,
)

db = SessionLocal()

try:

    news_articles = (
        NewsArticleRepository(db)
        .get_history(
            "RELIANCE"
        )
    )

    news_features = (
        NewsFeatureBuilder.build(
            news_articles
        )
    )

    print(
        "News Feature Rows:",
        len(news_features)
    )

    print(
        news_features.head()
    )

    print(
        news_features.tail()
    )

finally:

    db.close()