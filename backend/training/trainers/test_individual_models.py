from database.session import SessionLocal
from repositories.ohlcv_repository import OHLCVRepository

from forecasting.train_xgboost import train


def test_all_models():

    db = SessionLocal()

    try:

        symbols = (
            OHLCVRepository(db)
            .get_all_symbols()
        )

    finally:

        db.close()

    print(
        f"\nTotal Symbols: {len(symbols)}"
    )

    results = []

    for index, symbol in enumerate(
        symbols,
        start=1,
    ):

        print("\n" + "=" * 60)
        print(
            f"Training {index}/{len(symbols)}: {symbol}"
        )

        try:

            result = train(
                symbol=symbol,
                horizon="5d",
            )

            results.append(result)

            print("\nReturned Metrics:")
            print(result)

        except Exception as e:

            print(
                f"\nFAILED: {symbol}"
            )

            print(str(e))

    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    for result in results:

        print(result)

    assert True