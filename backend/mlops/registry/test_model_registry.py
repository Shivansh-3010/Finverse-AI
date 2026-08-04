from model_registry import (
    ModelRegistry,
)


def test():

    ModelRegistry.register(

        model_name="xgboost",

        symbol="RELIANCE",

        horizon="1d",

        version="1.0.0",

        metrics={
            "mae":1.21,
            "rmse":2.03,
            "directional_accuracy":74.5,
        },

        artifact_path=(
            "backend/models/xgboost/"
            "reliance_xgb_1d.pkl"
        ),
    )

    registry = (
        ModelRegistry.load(
            "xgboost",
            "RELIANCE",
            "1d",
        )
    )

    assert registry is not None

    assert (
        registry["symbol"]
        == "RELIANCE"
    )

    assert (
        registry["version"]
        == "1.0.0"
    )

    assert (
        ModelRegistry.exists(
            "xgboost",
            "RELIANCE",
            "1d",
        )
    )

    print()

    print(registry)

    print()

    print(
        ModelRegistry.list_models()
    )


if __name__ == "__main__":

    test()