from mlops.evaluation.metrics import (
    MetricsEngine,
)


def test_metrics():

    y_true = [100, 105, 110, 115]
    y_pred = [102, 104, 111, 114]

    print(
        "MAE:",
        MetricsEngine.mae(
            y_true,
            y_pred
        )
    )

    print(
        "RMSE:",
        MetricsEngine.rmse(
            y_true,
            y_pred
        )
    )

    print(
        "MAPE:",
        MetricsEngine.mape(
            y_true,
            y_pred
        )
    )

    print(
        "Directional Accuracy:",
        MetricsEngine.directional_accuracy(
            y_true,
            y_pred
        )
    )


if __name__ == "__main__":
    test_metrics()