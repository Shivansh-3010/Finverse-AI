from database.session import SessionLocal

from forecasting.dataset_builder import (
    DatasetBuilder,
)

from forecasting.horizons import (
    HORIZON_DAYS,
)

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

import pandas as pd


def test_target_values():

    db = SessionLocal()

    try:

        records = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe(
                "RELIANCE",
                "1d",
            )
        )

        patterns = (
            CandlestickPatternRepository(db)
            .get_history_by_timeframe(
                "RELIANCE",
                "1d",
            )
        )

        df = ohlcv_to_dataframe(records)

        candlestick_features = pd.DataFrame(
            [
                {
                    "timestamp": p.timestamp,
                    "strength": p.strength,
                    "confidence": p.confidence,
                    "candlestick_score": p.candlestick_score,
                }
                for p in patterns
            ]
        )

        dataset = DatasetBuilder.build(
            df,
            candlestick_features,
            horizon_days=HORIZON_DAYS["1d"],
        )

        target = dataset["target"]

        print("\nTarget Summary")

        print(
            "Zero Count:",
            (target == 0).sum()
        )

        print(
            "Non-Zero Count:",
            (target != 0).sum()
        )

        print(
            "\nFirst 20 Targets:"
        )

        print(
            target.head(20).tolist()
        )

    finally:
        db.close()