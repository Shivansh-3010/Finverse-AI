import pandas as pd

from database.session import SessionLocal

from models.ohlcv_data import OHLCVData

from risk.historical_risk_engine import (
    HistoricalRiskEngine
)

SYMBOL = "RELIANCE"


def main():

    db = SessionLocal()

    try:

        candles = (
            db.query(OHLCVData)
            .filter(
                OHLCVData.symbol == SYMBOL,
                OHLCVData.timeframe == "1d"
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
                "close": [
                    c.close
                    for c in candles
                ]
            }
        )

        risk_df = (
            HistoricalRiskEngine
            .build_features(
                df["close"]
            )
        )

        risk_df["timestamp"] = (
            df["timestamp"]
        )

        risk_df = risk_df.dropna()

        print(
            f"Risk rows: {len(risk_df)}"
        )

        print(
            risk_df[
                [
                    "volatility_252d",
                    "volatility_504d",
                    "expected_shortfall_252d",
                    "expected_shortfall_504d"
                ]
            ].tail()
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()