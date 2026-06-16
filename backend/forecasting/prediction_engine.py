import pandas as pd

from forecasting.model_loader import (
    ModelLoader,
)


class PredictionEngine:

    def __init__(self):

        self.model = (
            ModelLoader.load_model()
        )

        self.features = (
            ModelLoader.load_features()
        )

    def predict(
        self,
        feature_dict: dict
    ):

        row = []

        for feature in self.features:

            row.append(
                feature_dict.get(
                    feature,
                    0.0
                )
            )

        X = pd.DataFrame(
            [row],
            columns=self.features
        )

        prediction = (
            self.model.predict(X)[0]
        )

        return float(
            prediction
        )