from forecasting.lstm_dataset_builder import (
    LSTMDatasetBuilder,
)

from forecasting.lstm_trainer import (
    LSTMTrainer,
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

    model = (
        LSTMTrainer.train(
            X,
            y,
            epochs=5,
        )
    )

    print(
        type(model).__name__
    )


if __name__ == "__main__":
    test()