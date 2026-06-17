from forecasting.lstm_dataset_builder import (
    LSTMDatasetBuilder,
)


def test():

    prices = list(
        range(
            100
        )
    )

    X, y = (
        LSTMDatasetBuilder.build(
            prices=prices,
            sequence_length=30,
        )
    )

    print(
        "X Shape:",
        X.shape
    )

    print(
        "Y Shape:",
        y.shape
    )


if __name__ == "__main__":
    test()