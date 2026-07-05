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

from training.universe.universe_selector import (
    UniverseSelector,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

import pandas as pd


def test_target_distribution():

    db = SessionLocal()

    try:

        symbols = (
            UniverseSelector.get_symbols(
                db=db,
                timeframe="1d",
                min_candles=5000,
            )[:5]
        )

        for symbol in symbols:

            records = (
                OHLCVRepository(db)
                .get_history_by_symbol_and_timeframe(
                    symbol,
                    "1d",
                )
            )

            patterns = (
                CandlestickPatternRepository(db)
                .get_history_by_timeframe(
                    symbol,
                    "1d",
                )
            )

            df = ohlcv_to_dataframe(
                records
            )

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

            positive_pct = (
                (target > 0).mean() * 100
            )

            negative_pct = (
                (target < 0).mean() * 100
            )

            print("\n" + "=" * 60)

            print("Symbol:", symbol)

            print(
                "Rows:",
                len(dataset)
            )

            print(
                "Mean:",
                round(target.mean(), 4)
            )

            print(
                "Std:",
                round(target.std(), 4)
            )

            print(
                "Positive %:",
                round(
                    positive_pct,
                    2
                )
            )

            print(
                "Negative %:",
                round(
                    negative_pct,
                    2
                )
            )

    finally:
        db.close()