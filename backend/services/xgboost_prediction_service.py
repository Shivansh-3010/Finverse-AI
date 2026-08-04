import pandas as pd


class XGBoostPredictionService:

    @staticmethod
    def predict(
        model,
        X: pd.DataFrame,
    ):

        predictions = model.predict(X)

        return [
            float(value)
            for value in predictions
        ]