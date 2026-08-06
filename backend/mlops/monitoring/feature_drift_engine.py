import numpy as np


class FeatureDriftEngine:

    @staticmethod
    def calculate(
        training_data,
        production_data,
    ):
        """
        Computes simple feature drift based on
        mean and standard deviation changes.
        """

        report = {}

        for column in training_data.columns:

            if column not in production_data.columns:
                continue

            train = (
                training_data[column]
                .dropna()
                .astype(float)
            )

            prod = (
                production_data[column]
                .dropna()
                .astype(float)
            )

            if len(train) == 0 or len(prod) == 0:
                continue

            train_mean = float(train.mean())
            prod_mean = float(prod.mean())

            train_std = float(train.std())
            prod_std = float(prod.std())

            mean_shift = abs(
                prod_mean - train_mean
            )

            std_shift = abs(
                prod_std - train_std
            )

            drift_score = (
                mean_shift +
                std_shift
            )

            report[column] = {

                "training_mean": round(
                    train_mean,
                    4,
                ),

                "production_mean": round(
                    prod_mean,
                    4,
                ),

                "training_std": round(
                    train_std,
                    4,
                ),

                "production_std": round(
                    prod_std,
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

        return report