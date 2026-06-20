from pathlib import Path

import pandas as pd

from repositories.ohlcv_repository import (
    OHLCVRepository,
)


class HistoricalOHLCVImportService:

    @staticmethod
    def import_csv(
        db,
        csv_path: str,
        timeframe: str = "1d",
        limit: int | None = None,
    ):

        csv_file = Path(csv_path)

        symbol = (
            csv_file.stem
            .upper()
            .replace(".NS", "")
        )

        df = pd.read_csv(
            csv_path
        )

        if limit:

            df = df.head(limit)

        repository = (
            OHLCVRepository(db)
        )

        records = []

        imported = 0
        skipped = 0

        for _, row in df.iterrows():

            try:

                timestamp = (
                    pd.to_datetime(
                        row["Date"]
                    )
                )

                dividend = float(
                    row.get(
                        "Dividends",
                        0.0
                    )
                )

                stock_split = float(
                    row.get(
                        "Stock Splits",
                        0.0
                    )
                )

                if repository.exists(
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=timestamp,
                ):

                    repository.update_corporate_actions(
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=timestamp,
                        dividend=dividend,
                        stock_split=stock_split,
                    )

                    skipped += 1
                    continue

                records.append(
                    {
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "timestamp": timestamp,

                        "open": float(
                            row["Open"]
                        ),

                        "high": float(
                            row["High"]
                        ),

                        "low": float(
                            row["Low"]
                        ),

                        "close": float(
                            row["Close"]
                        ),

                        "volume": int(
                            row["Volume"]
                        ),

                        "dividend": dividend,

                        "stock_split": stock_split,
                    }
                )

                imported += 1

                if imported % 1000 == 0:

                    print(
                        f"{symbol}: "
                        f"{imported:,} rows"
                    )

            except Exception as e:

                skipped += 1

                print(
                    f"Skipped row: {e}"
                )
        
        if records:

            repository.bulk_insert(
                records
            )

        return {

            "symbol": symbol,

            "imported": imported,

            "skipped": skipped,

            "total_rows": len(df),
        }