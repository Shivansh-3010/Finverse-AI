from database.session import SessionLocal
from models.news_article import NewsArticle

db = SessionLocal()

try:

    articles = (
        db.query(NewsArticle)
        .filter(
            NewsArticle.provider ==
            "sentiment_dataset"
        )
        .limit(5)
        .all()
    )

    for article in articles:

        print("=" * 80)

        print("TITLE:")
        print(article.title)

        print("\nSENTIMENT:")
        print(article.sentiment)

        print("\nCONFIDENCE:")
        print(article.confidence)

        print("\nEVENTS:")
        print(article.events)

        print("\nNEWS SCORE:")
        print(article.news_score)

finally:

    db.close()