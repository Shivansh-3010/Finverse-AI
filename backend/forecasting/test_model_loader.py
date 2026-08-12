from forecasting.model_loader import ModelLoader


def test_load_model_and_features():
    model = ModelLoader.load_model(
        model_type="xgboost",
        symbol="RELIANCE",
        horizon="5d",
    )

    print(type(model).__name__)

    features = ModelLoader.load_features(
        symbol="RELIANCE",
        horizon="5d",
    )

    print(len(features))

    assert model is not None
    assert features