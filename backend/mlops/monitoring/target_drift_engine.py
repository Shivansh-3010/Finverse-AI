import numpy as np

from scipy.stats import ks_2samp


class TargetDriftEngine:

    SIGNIFICANCE_LEVEL = 0.05

    @staticmethod
    def calculate(
        historical_targets,
        recent_targets,
    ):
        """
        Compare historical and recent target
        distributions using the two-sample KS test.

        For FinVerse, the target represents actual
        realized returns.
        """

        historical = np.asarray(
            historical_targets,
            dtype=float,
        )

        recent = np.asarray(
            recent_targets,
            dtype=float,
        )

        historical = historical[
            np.isfinite(historical)
        ]

        recent = recent[
            np.isfinite(recent)
        ]

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
            recent_mean
            - historical_mean
        )

        std_shift = abs(
            recent_std
            - historical_std
        )

        ks_result = ks_2samp(
            historical,
            recent,
        )

        ks_statistic = float(
            ks_result.statistic
        )

        p_value = float(
            ks_result.pvalue
        )

        drift_detected = (
            p_value
            < TargetDriftEngine
            .SIGNIFICANCE_LEVEL
        )

        if ks_statistic < 0.10:
            severity = "LOW"

        elif ks_statistic < 0.25:
            severity = "MEDIUM"

        elif ks_statistic < 0.50:
            severity = "HIGH"

        else:
            severity = "CRITICAL"

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

            "ks_statistic": round(
                ks_statistic,
                4,
            ),

            "p_value": round(
                p_value,
                6,
            ),

            "drift_score": round(
                ks_statistic,
                4,
            ),

            "severity": severity,

            "drift_detected":
                drift_detected,
        }