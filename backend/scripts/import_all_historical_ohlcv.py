from pathlib import Path

from database.session import SessionLocal

from services.historical_ohlcv_import_service import (
    HistoricalOHLCVImportService,
)

DATASET_DIR = Path(
    r"C:\Projects\Finverse-AI\datasets\OHLCV\NIFTY-50 Stock Market Data (2000 - 2021)"
)


def main():

    db = SessionLocal()

    try:

        total_files = 0
        total_imported = 0
        total_skipped = 0

        csv_files = [

            csv_file

            for csv_file in sorted(
                DATASET_DIR.glob("*.csv")
            )

            if csv_file.name != "NIFTY50_all.csv"
        ]

        print(
            f"Found {len(csv_files)} files"
        )

        for csv_file in csv_files:

            print(
                f"\nProcessing: {csv_file.name}"
            )

            result = (
                HistoricalOHLCVImportService
                .import_csv(
                    db=db,
                    csv_path=str(csv_file),
                    timeframe="1d",
                )
            )

            total_files += 1

            total_imported += (
                result["imported"]
            )

            total_skipped += (
                result["skipped"]
            )

            print(
                f"Imported: "
                f"{result['imported']:,}"
            )

            print(
                f"Skipped: "
                f"{result['skipped']:,}"
            )

        print("\n" + "=" * 80)

        print(
            "FILES PROCESSED:",
            total_files
        )

        print(
            "TOTAL IMPORTED:",
            f"{total_imported:,}"
        )

        print(
            "TOTAL SKIPPED:",
            f"{total_skipped:,}"
        )

        print("=" * 80)

    finally:

        db.close()


if __name__ == "__main__":
    main()