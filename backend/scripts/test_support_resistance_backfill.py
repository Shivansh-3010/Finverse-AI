import pandas as pd

from database.session import SessionLocal

from models.ohlcv_data import OHLCVData

from technical.support_resistance.historical_support_resistance_engine import (
    HistoricalSupportResistanceEngine,
)

SYMBOL = "RELIANCE"


def main():

    db = SessionLocal()

    try:

        candles = (
            db.query(OHLCVData)
            .filter(
                OHLCVData.symbol == SYMBOL,
                OHLCVData.timeframe == "1d",
            )
            .order_by(
                OHLCVData.timestamp
            )
            .all()
        )

        print(
            f"Candles: {len(candles)}"
        )

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

        sr_df["timestamp"] = (
            df["timestamp"].iloc[
                HistoricalSupportResistanceEngine.LOOKBACK_WINDOW:
            ].to_numpy()
        )

        print(
            f"Support/Resistance rows: {len(sr_df)}"
        )

        print(
            sr_df[
                [
                    "nearest_support",
                    "nearest_resistance",
                    "distance_to_support_pct",
                    "distance_to_resistance_pct",
                    "support_strength",
                    "resistance_strength",
                    "signal",
                ]
            ]
            .tail()
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()