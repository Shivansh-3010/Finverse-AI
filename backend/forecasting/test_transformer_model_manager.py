from forecasting.transformer_engine import (
    TransformerEngine,
)

from forecasting.transformer_model_manager import (
    TransformerModelManager,
)


def test():

    model = TransformerEngine()

    TransformerModelManager.save(
        model,
        "models/transformer/transformer_model.pt",
    )

    loaded_model = (
        TransformerModelManager.load(
            TransformerEngine(),
            "models/transformer/transformer_model.pt",
        )
    )

    print(
        type(
            loaded_model
        ).__name__
    )


if __name__ == "__main__":
    test()