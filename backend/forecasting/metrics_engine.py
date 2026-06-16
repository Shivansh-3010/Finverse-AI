import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)


class MetricsEngine:

    @staticmethod
    def mae(
        y_true,
        y_pred
    ) -> float:

        return float(
            mean_absolute_error(
                y_true,
                y_pred
            )
        )

    @staticmethod
    def rmse(
        y_true,
        y_pred
    ) -> float:

        return float(
            np.sqrt(
                mean_squared_error(
                    y_true,
                    y_pred
                )
            )
        )

    @staticmethod
    def mape(
        y_true,
        y_pred
    ) -> float:

        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        non_zero_mask = y_true != 0

        return float(
            np.mean(
                np.abs(
                    (
                        y_true[non_zero_mask]
                        - y_pred[non_zero_mask]
                    )
                    /
                    y_true[non_zero_mask]
                )
            ) * 100
        )

    @staticmethod
    def directional_accuracy(
        y_true,
        y_pred
    ) -> float:

        true_direction = np.sign(
            np.diff(y_true)
        )

        pred_direction = np.sign(
            np.diff(y_pred)
        )

        return float(
            (
                true_direction
                == pred_direction
            ).mean()
            * 100
        )