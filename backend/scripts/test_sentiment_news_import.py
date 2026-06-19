from database.session import SessionLocal

from services.sentiment_news_import_service import (
    SentimentNewsImportService,
)

db = SessionLocal()

try:

    result = (
        SentimentNewsImportService.import_csv(
            db=db,
            csv_path=
                r"C:\Projects\Finverse-AI\datasets\historical_news\News_sentiment_Jan2017_to_Apr2021.csv",
            limit=None,
        )
    )

    print(result)

finally:

    db.close()