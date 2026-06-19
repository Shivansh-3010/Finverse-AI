from pathlib import Path

from database.session import SessionLocal

from services.company_news_import_service import (
    CompanyNewsImportService,
)

DATASET_DIR = (
    Path(
        r"C:\Projects\Finverse-AI\datasets\company_news"
    )
)

db = SessionLocal()

try:

    total_imported = 0
    total_files = 0

    for csv_file in sorted(
        DATASET_DIR.glob("*.csv")
    ):

        print(
            f"\nProcessing: {csv_file.name}"
        )

        result = (
            CompanyNewsImportService.import_csv(
                db=db,
                csv_path=str(csv_file),
            )
        )

        total_imported += (
            result["imported"]
        )

        total_files += 1

    print("\n" + "=" * 80)

    print(
        "FILES PROCESSED:",
        total_files
    )

    print(
        "TOTAL IMPORTED:",
        total_imported
    )

    print("=" * 80)

finally:

    db.close()