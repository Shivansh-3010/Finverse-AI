from pathlib import Path

from database.session import SessionLocal

from services.historical_ohlcv_import_service import (
    HistoricalOHLCVImportService,
)


DATASET_DIR = Path(
    r"C:\Projects\Finverse-AI\datasets\OHLCV\NSE-stock-market-historical-data\v1"
)


def main():

    csv_files = sorted(
        DATASET_DIR.glob("*.csv")
    )

    print(
        f"Found {len(csv_files)} files"
    )

    total_imported = 0
    total_skipped = 0
    processed = 0

    db = SessionLocal()

    try:

        for csv_file in csv_files:

            processed += 1

            print(
                "\n"
                + "=" * 80
            )

            print(
                f"[{processed}/{len(csv_files)}] "
                f"{csv_file.name}"
            )

            try:

                result = (
                    HistoricalOHLCVImportService.import_csv(
                        db=db,
                        csv_path=str(csv_file),
                        timeframe="1d",
                    )
                )

                total_imported += result[
                    "imported"
                ]

                total_skipped += result[
                    "skipped"
                ]

                print(result)

            except Exception as e:

                print(
                    f"FAILED: {csv_file.name}"
                )

                print(e)

        print(
            "\n"
            + "=" * 80
        )

        print(
            f"FILES PROCESSED: {processed:,}"
        )

        print(
            f"TOTAL IMPORTED: {total_imported:,}"
        )

        print(
            f"TOTAL SKIPPED: {total_skipped:,}"
        )

        print(
            "=" * 80
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()