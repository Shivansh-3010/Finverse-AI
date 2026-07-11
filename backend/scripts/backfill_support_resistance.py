from tqdm import tqdm

import pandas as pd

from database.session import SessionLocal

from models.ohlcv_data import OHLCVData
from models.support_resistance import (
    SupportResistance,
)

from repositories.support_resistance_repository import (
    SupportResistanceRepository,
)

from technical.support_resistance.historical_support_resistance_engine import (
    HistoricalSupportResistanceEngine,
)


def main():

    db = SessionLocal() 

    repository = (
        SupportResistanceRepository(db)
    )

    try:

        symbols = [
            row[0]
            for row in (
                db.query(
                    OHLCVData.symbol
                )
                .distinct()
                .all()
            )
        ]

        total_inserted = 0

        for symbol in tqdm(symbols):
            
            existing = (
                db.query(
                    SupportResistance
                )
                .filter(
                    SupportResistance.symbol == symbol,
                    SupportResistance.timeframe == "1d",
                )
                .first()
            )

            if existing:
                print(
                    f"Skipping {symbol}"
                )
                continue

            candles = (
                db.query(OHLCVData)
                .filter(
                    OHLCVData.symbol == symbol,
                    OHLCVData.timeframe == "1d",
                )
                .order_by(
                    OHLCVData.timestamp
                )
                .all()
            )

            if (
                len(candles)
                <= HistoricalSupportResistanceEngine.LOOKBACK_WINDOW
            ):
                continue

            df = pd.DataFrame(
                {
                    "timestamp": [
                        c.timestamp
                        for c in candles
                    ],
                    "open": [
                        c.open
                        for c in candles
                    ],
                    "high": [
                        c.high
                        for c in candles
                    ],
                    "low": [
                        c.low
                        for c in candles
                    ],
                    "close": [
                        c.close
                        for c in candles
                    ],
                    "volume": [
                        c.volume
                        for c in candles
                    ],
                }
            )

            sr_df = (
                HistoricalSupportResistanceEngine
                .build_features(df)
            )
            
            if sr_df.empty:
                print(
                    f"No S&R levels found for {symbol}"
                )
                continue

            records = []

            for _, row in sr_df.iterrows():

                records.append(
                    SupportResistance(
                        symbol=symbol,
                        timeframe="1d",
                        timestamp=row["timestamp"],

                        nearest_support=row[
                            "nearest_support"
                        ],

                        nearest_resistance=row[
                            "nearest_resistance"
                        ],

                        distance_to_support_pct=row[
                            "distance_to_support_pct"
                        ],

                        distance_to_resistance_pct=row[
                            "distance_to_resistance_pct"
                        ],

                        support_strength=row[
                            "support_strength"
                        ],

                        resistance_strength=row[
                            "resistance_strength"
                        ],

                        breakout_zone_lower=row[
                            "breakout_zone_lower"
                        ],

                        breakout_zone_upper=row[
                            "breakout_zone_upper"
                        ],

                        breakdown_zone_lower=row[
                            "breakdown_zone_lower"
                        ],

                        breakdown_zone_upper=row[
                            "breakdown_zone_upper"
                        ],

                        signal=row["signal"],

                        signal_level=row[
                            "signal_level"
                        ],
                    )
                )

            repository.bulk_insert(
                records
            )

            total_inserted += len(
                records
            )

        print(
            f"Inserted {total_inserted} rows"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()