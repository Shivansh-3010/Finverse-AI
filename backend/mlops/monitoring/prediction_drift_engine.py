import numpy as np


class PredictionDriftEngine:

    @staticmethod
    def calculate(
        historical_predictions,
        recent_predictions,
    ):
        """
        Compare historical prediction distribution
        against current production predictions.
        """

        historical = np.asarray(
            historical_predictions,
            dtype=float,
        )

        recent = np.asarray(
            recent_predictions,
            dtype=float,
        )

        if (
            historical.size == 0
            or recent.size == 0
        ):
            return {}

        historical_mean = float(
            np.mean(historical)
        )

        recent_mean = float(
            np.mean(recent)
        )

        historical_std = float(
            np.std(historical)
        )

        recent_std = float(
            np.std(recent)
        )

        mean_shift = abs(
            recent_mean - historical_mean
        )

        std_shift = abs(
            recent_std - historical_std
        )

        drift_score = (
            mean_shift
            +
            std_shift
        )

        return {

            "historical_mean": round(
                historical_mean,
                4,
            ),

            "recent_mean": round(
                recent_mean,
                4,
            ),

            "historical_std": round(
                historical_std,
                4,
            ),

            "recent_std": round(
                recent_std,
                4,
            ),

            "mean_shift": round(
                mean_shift,
                4,
            ),

            "std_shift": round(
                std_shift,
                4,
            ),

            "drift_score": round(
                drift_score,
                4,
            ),

            "drift_detected": (
                drift_score > 1.0
            ),
        }