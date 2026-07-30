from pathlib import Path

import joblib


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

XGBOOST_MODEL_DIR = (
    PROJECT_ROOT
    / "models"
    / "xgboost"
)

PROPHET_MODEL_DIR = (
    PROJECT_ROOT
    / "models"
    / "prophet"
)


class ModelLoader:

    @staticmethod
    def load_model(
        model_type: str = "xgboost",
        symbol: str = "RELIANCE",
        horizon: str = "1d",
    ):

        model_type = model_type.lower()
        symbol = symbol.upper()

        if model_type == "xgboost":
            return joblib.load(
                XGBOOST_MODEL_DIR /
                f"{symbol.lower()}_xgb_{horizon}.pkl"
            )

        if model_type == "prophet":
            return joblib.load(
                PROPHET_MODEL_DIR /
                f"{symbol}_{horizon}.joblib"
            )

        raise ValueError(
            f"Unsupported model type: {model_type}"
        )

    @staticmethod
    def load_features(
        symbol: str = "RELIANCE",
        horizon: str = "1d",
    ):

        symbol = symbol.lower()

        return joblib.load(
            XGBOOST_MODEL_DIR /
            f"{symbol}_xgb_features_{horizon}.pkl"
        )