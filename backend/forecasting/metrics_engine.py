import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)


class MetricsEngine:

    MAPE_EPSILON = 1e-4

    @staticmethod
    def mae(
        y_true,
        y_pred,
    ) -> float:

        y_true = np.asarray(
            y_true,
            dtype=float,
        )

        y_pred = np.asarray(
            y_pred,
            dtype=float,
        )

        return float(
            mean_absolute_error(
                y_true,
                y_pred,
            )
        )

    @staticmethod
    def rmse(
        y_true,
        y_pred,
    ) -> float:

        y_true = np.asarray(
            y_true,
            dtype=float,
        )

        y_pred = np.asarray(
            y_pred,
            dtype=float,
        )

        return float(
            np.sqrt(
                mean_squared_error(
                    y_true,
                    y_pred,
                )
            )
        )

    @staticmethod
    def mape(
        y_true,
        y_pred,
    ) -> float:

        y_true = np.asarray(
            y_true,
            dtype=float,
        )

        y_pred = np.asarray(
            y_pred,
            dtype=float,
        )

        valid_mask = (
            np.isfinite(y_true)
            & np.isfinite(y_pred)
            & (
                np.abs(y_true)
                >= MetricsEngine.MAPE_EPSILON
            )
        )

        if not np.any(valid_mask):
            return 0.0

        actual = y_true[valid_mask]
        predicted = y_pred[valid_mask]

        percentage_errors = (
            np.abs(
                actual - predicted
            )
            /
            np.abs(actual)
        )

        return float(
            np.mean(
                percentage_errors
            ) * 100
        )

    @staticmethod
    def smape(
        y_true,
        y_pred,
    ) -> float:

        y_true = np.asarray(
            y_true,
            dtype=float,
        )

        y_pred = np.asarray(
            y_pred,
            dtype=float,
        )

        denominator = (
            np.abs(y_true)
            +
            np.abs(y_pred)
        )

        valid_mask = (
            np.isfinite(y_true)
            & np.isfinite(y_pred)
            & (denominator > 0)
        )

        if not np.any(valid_mask):
            return 0.0

        numerator = (
            2.0
            * np.abs(
                y_pred[valid_mask]
                - y_true[valid_mask]
            )
        )

        denominator = denominator[
            valid_mask
        ]

        return float(
            np.mean(
                numerator
                / denominator
            )
            * 100
        )

    @staticmethod
    def directional_accuracy(
        y_true,
        y_pred,
    ) -> float:

        y_true = np.asarray(
            y_true,
            dtype=float,
        )

        y_pred = np.asarray(
            y_pred,
            dtype=float,
        )

        valid_mask = (
            np.isfinite(y_true)
            & np.isfinite(y_pred)
        )

        if not np.any(valid_mask):
            return 0.0

        actual = y_true[valid_mask]
        predicted = y_pred[valid_mask]

        true_direction = np.sign(
            actual
        )

        predicted_direction = np.sign(
            predicted
        )

        return float(
            np.mean(
                true_direction
                == predicted_direction
            )
            * 100
        )