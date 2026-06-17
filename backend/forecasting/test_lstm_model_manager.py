from forecasting.lstm_engine import (
    LSTMEngine,
)

from forecasting.lstm_model_manager import (
    LSTMModelManager,
)


def test():

    model = LSTMEngine()

    LSTMModelManager.save(
        model,
        "models/lstm_model.pt",
    )

    loaded_model = (
        LSTMModelManager.load(
            LSTMEngine(),
            "models/lstm_model.pt",
        )
    )

    print(
        type(
            loaded_model
        ).__name__
    )


if __name__ == "__main__":
    test()