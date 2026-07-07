import pandas as pd
from tqdm import tqdm

from database.session import SessionLocal

from models.ohlcv_data import OHLCVData
from models.risk_metric import RiskMetric

from repositories.risk_metric_repository import (
    RiskMetricRepository
)

from risk.historical_risk_engine import (
    HistoricalRiskEngine
)

BATCH_SIZE = 1000


def main():

    db = SessionLocal()

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

        repository = (
            RiskMetricRepository(db)
        )

        total_inserted = 0

        for symbol in tqdm(symbols):

            candles = (
                db.query(OHLCVData)
                .filter(
                    OHLCVData.symbol == symbol,
                    OHLCVData.timeframe == "1d"
                )
                .order_by(
                    OHLCVData.timestamp
                )
                .all()
            )

            if len(candles) < 504:
                continue

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

            objects = []

            for row in risk_df.to_dict(
                orient="records"
            ):

                objects.append(
                    RiskMetric(
                        symbol=symbol,
                        timeframe="1d",
                        timestamp=row[
                            "timestamp"
                        ],
                        volatility_252d=row[
                            "volatility_252d"
                        ],
                        volatility_504d=row[
                            "volatility_504d"
                        ],
                        drawdown_252d=row[
                            "drawdown_252d"
                        ],
                        drawdown_504d=row[
                            "drawdown_504d"
                        ],
                        var95_252d=row[
                            "var95_252d"
                        ],
                        var95_504d=row[
                            "var95_504d"
                        ],
                        expected_shortfall_252d=row[
                            "expected_shortfall_252d"
                        ],

                        expected_shortfall_504d=row[
                            "expected_shortfall_504d"
                        ],

                        risk_score=int(
                            row["risk_score"]
                        ),

                        risk_category=row[
                            "risk_category"
                        ]
                    )
                )

                if len(objects) >= BATCH_SIZE:

                    repository.bulk_insert(
                        objects
                    )

                    total_inserted += (
                        len(objects)
                    )

                    objects = []

            if objects:

                repository.bulk_insert(
                    objects
                )

                total_inserted += (
                    len(objects)
                )

        print(
            f"Inserted {total_inserted} rows"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()