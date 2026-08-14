import numpy as np
from scipy.stats import ks_2samp


class FeatureDriftEngine:

    SIGNIFICANCE_LEVEL = 0.05

    @staticmethod
    def calculate(
        training_data,
        production_data,
    ):
        """
        Compare training and production feature
        distributions using the two-sample KS test.

        The returned drift_score is the KS statistic,
        which is normalized between 0 and 1.
        """

        report = {}

        for column in training_data.columns:

            if column not in production_data.columns:
                continue

            train = (
                training_data[column]
                .dropna()
                .astype(float)
                .to_numpy()
            )

            prod = (
                production_data[column]
                .dropna()
                .astype(float)
                .to_numpy()
            )

            if len(train) == 0 or len(prod) == 0:
                continue

            training_mean = float(
                np.mean(train)
            )

            production_mean = float(
                np.mean(prod)
            )

            training_std = float(
                np.std(train)
            )

            production_std = float(
                np.std(prod)
            )

            mean_shift = abs(
                production_mean
                - training_mean
            )

            std_shift = abs(
                production_std
                - training_std
            )

            ks_result = ks_2samp(
                train,
                prod,
            )

            ks_statistic = float(
                ks_result.statistic
            )

            p_value = float(
                ks_result.pvalue
            )

            drift_detected = (
                p_value
                < FeatureDriftEngine
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

            report[column] = {

                "training_mean": round(
                    training_mean,
                    4,
                ),

                "production_mean": round(
                    production_mean,
                    4,
                ),

                "training_std": round(
                    training_std,
                    4,
                ),

                "production_std": round(
                    production_std,
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

        return report