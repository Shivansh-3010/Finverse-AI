import pandas as pd

from services.xgboost_training_service import (
    XGBoostTrainingService,
)


def test():

    X = pd.DataFrame(
        {
            "a": range(50),
            "b": range(50, 100),
        }
    )

    y = (
        X["a"] * 0.25
        + X["b"] * 0.75
    )

    model = (
        XGBoostTrainingService.train(
            X,
            y,
        )
    )

    prediction = (
        model.predict(
            X.iloc[:5]
        )
    )

    assert len(prediction) == 5

    print(prediction)