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
    def load_model():

        return joblib.load(
            MODEL_DIR /
            "reliance_xgb.pkl"
        )

    @staticmethod
    def load_features():

        return joblib.load(
            MODEL_DIR /
            "reliance_xgb_features.pkl"
        )