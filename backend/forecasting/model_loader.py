from pathlib import Path

import joblib


MODEL_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
    / "models"
    / "xgboost"
)


class ModelLoader:

    @staticmethod
    def load_model(
        horizon: str = "1d",
    ):

        return joblib.load(
            MODEL_DIR /
            f"reliance_xgb_{horizon}.pkl"
        )

    @staticmethod
    def load_features(
        horizon: str = "1d",
    ):

        return joblib.load(
            MODEL_DIR /
            f"reliance_xgb_features_{horizon}.pkl"
        )