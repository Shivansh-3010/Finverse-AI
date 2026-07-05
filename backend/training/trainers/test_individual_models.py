from forecasting.train_xgboost import train


def test_individual_models():

    symbols = [
        "RELIANCE",
        "INFY",
        "TCS",
        "SBIN",
        "HDFCBANK",
    ]

    for symbol in symbols:

        print("\n" + "=" * 60)
        print("Training:", symbol)

        train(
            symbol=symbol,
            horizon="1d",
        )

    assert True