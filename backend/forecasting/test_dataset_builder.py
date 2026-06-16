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

        dataset = (
            DatasetBuilder.build(df)
        )

        print(
            "Rows:",
            len(dataset)
        )

        print(
            dataset.tail()
        )

    finally:
        db.close()


if __name__ == "__main__":
    test_dataset_builder()