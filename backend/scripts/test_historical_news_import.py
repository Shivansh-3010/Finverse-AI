from database.session import (
    SessionLocal,
)

from services.historical_news_import_service import (
    HistoricalNewsImportService,
)

db = SessionLocal()

try:

    result = (
        HistoricalNewsImportService.import_csv(
            db=db,

            csv_path=
            r"C:\Projects\Finverse-AI\datasets\historical_news\IndianFinancialNews.csv",

            limit=50000,
        )
    )

    print(result)

finally:

    db.close()