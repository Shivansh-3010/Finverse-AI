import pandas as pd

from services.xgboost_training_service import (
    XGBoostTrainingService,
)

from services.xgboost_prediction_service import (
    XGBoostPredictionService,
)


def test():

    X = pd.DataFrame(
        {
            "a": range(50),
            "b": range(50, 100),
        }
    )

    y = (
        X["a"] * 0.5
        + X["b"] * 0.5
    )

    model = (
        XGBoostTrainingService.train(
            X,
            y,
        )
    )

    predictions = (
        XGBoostPredictionService.predict(
            model,
            X.iloc[:10],
        )
    )

    assert len(predictions) == 10

    print(predictions)