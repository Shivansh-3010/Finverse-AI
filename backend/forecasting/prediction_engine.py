import pandas as pd

from forecasting.model_loader import ModelLoader


class PredictionEngine:

    def __init__(
        self,
        model_type: str = "xgboost",
        symbol: str = "RELIANCE",
        horizon: str = "1d",
    ):

        self.model_type = model_type.lower()
        self.symbol = symbol
        self.horizon = horizon

        self.model = ModelLoader.load_model(
            model_type=self.model_type,
            symbol=self.symbol,
            horizon=self.horizon,
        )

        if self.model_type == "xgboost":
            self.features = ModelLoader.load_features(
                symbol=self.symbol,
                horizon=self.horizon,
            )
        else:
            self.features = None

    def predict(
        self,
        feature_dict: dict,
    ):

        if self.model_type == "xgboost":

            row = [
                feature_dict.get(feature, 0.0)
                for feature in self.features
            ]

            X = pd.DataFrame(
                [row],
                columns=self.features,
            )

            prediction = self.model.predict(X)[0]

            return float(prediction)

        raise NotImplementedError(
            f"Prediction not implemented for '{self.model_type}'."
        )