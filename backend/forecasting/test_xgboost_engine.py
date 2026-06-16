import numpy as np

from backend.forecasting.xgboost_engine import (
    XGBoostEngine,
)


def test_xgboost():

    X = np.array([
        [30, 1000],
        [35, 1200],
        [40, 1400],
        [45, 1600],
        [50, 1800],
    ])

    y = np.array([
        102,
        105,
        108,
        112,
        115,
    ])

    model = (
        XGBoostEngine.build_model()
    )

    model.fit(X, y)

    prediction = model.predict(
        [[42, 1500]]
    )

    print(
        "Prediction:",
        float(prediction[0])
    )


if __name__ == "__main__":
    test_xgboost()