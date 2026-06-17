import torch

from forecasting.lstm_engine import (
    LSTMEngine,
)


def test():

    model = LSTMEngine()

    sample = torch.randn(
        4,
        30,
        1
    )

    output = model(sample)

    print(
        output.shape
    )


if __name__ == "__main__":
    test()