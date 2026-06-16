import pandas as pd
from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

from forecasting.dataset_builder import (
    DatasetBuilder,
)
from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)

def test_dataset_builder():

    db = SessionLocal()

    try:

        records = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe(
                symbol="RELIANCE",
                timeframe="1d"
            )
        )

        df = ohlcv_to_dataframe(
            records
        )
        
        patterns = (
            CandlestickPatternRepository(db)
            .get_history_by_timeframe(
                "RELIANCE",
                "1d"
            )
        )

        candlestick_features = pd.DataFrame([
            {
                "timestamp": p.timestamp,
                "strength": p.strength,
                "confidence": p.confidence,
                "candlestick_score": p.candlestick_score,
            }
            for p in patterns
        ])

        dataset = (
            DatasetBuilder.build(
                df,
                candlestick_features
            )
        )

        print(
            "Rows:",
            len(dataset)
        )
        
        print(dataset.columns.tolist())

        print(
            dataset.tail()
        )

    finally:
        db.close()


if __name__ == "__main__":
    test_dataset_builder()