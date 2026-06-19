from forecasting.model_loader import (
    ModelLoader,
)

model = (
    ModelLoader.load_model(
        "5d"
    )
)

print(
    type(model).__name__
)

features = (
    ModelLoader.load_features(
        "5d"
    )
)

print(
    len(features)
)