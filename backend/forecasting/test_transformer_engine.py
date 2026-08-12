import torch

from forecasting.transformer_engine import (
    TransformerEngine,
)


def test():

    model = TransformerEngine(
        input_size=1
    )

    sample = torch.randn(
        4,
        30,
        1,
    )

    output = model(
        sample
    )

    print(
        output.shape
    )


if __name__ == "__main__":
    test()