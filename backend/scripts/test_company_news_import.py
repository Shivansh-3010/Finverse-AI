from database.session import SessionLocal

from services.company_news_import_service import (
    CompanyNewsImportService,
)

db = SessionLocal()

try:

    result = (
        CompanyNewsImportService.import_csv(
            db=db,

            csv_path=
                r"C:\Projects\Finverse-AI\datasets\company_news\reliance_industries_ri_news.csv",

            limit=10,
        )
    )

    print(result)

finally:

    db.close()