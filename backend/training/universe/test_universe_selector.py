from database.session import SessionLocal

from training.universe.universe_selector import (
    UniverseSelector,
)


def test_training_universe():

    db = SessionLocal()

    try:

        symbols = (
            UniverseSelector.get_symbols(
                db=db,
                timeframe="1d",
                min_candles=5000,
            )
        )

        print(
            "\nTraining Universe:",
            len(symbols)
        )

        print(
            symbols[:20]
        )

        assert len(symbols) > 0

    finally:
        db.close()