from forecasting.model_loader import (
    ModelLoader,
)


def test():

    model = (
        ModelLoader.load_model()
    )

    features = (
        ModelLoader.load_features()
    )

    print(
        "Model:",
        type(model).__name__
    )

    print(
        "Feature Count:",
        len(features)
    )

    print(
        features
    )


if __name__ == "__main__":
    test()