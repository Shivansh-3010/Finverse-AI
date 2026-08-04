from typing import Iterator
from collections.abc import Callable
from forecasting.metrics_engine import (
    MetricsEngine,
)

import pandas as pd



class WalkForwardEngine:

    @staticmethod
    def generate_windows(
        dataset: pd.DataFrame,
        train_size: int,
        test_size: int,
        step_size: int | None = None,
    ) -> Iterator[
        tuple[
            pd.DataFrame,
            pd.DataFrame,
        ]
    ]:

        if step_size is None:
            step_size = test_size

        total_rows = len(dataset)

        start = 0

        while True:

            train_end = (
                start + train_size
            )

            test_end = (
                train_end + test_size
            )

            if test_end > total_rows:
                break

            train_df = (
                dataset.iloc[
                    start:train_end
                ]
                .copy()
            )

            test_df = (
                dataset.iloc[
                    train_end:test_end
                ]
                .copy()
            )

            yield (
                train_df,
                test_df,
            )

            start += step_size
            
    @staticmethod
    def run(
        dataset: pd.DataFrame,
        train_size: int,
        test_size: int,
        train_callback: Callable,
        predict_callback: Callable,
        step_size: int | None = None,
    ):

        results = []

        for (
            train_df,
            test_df,
        ) in WalkForwardEngine.generate_windows(
            dataset=dataset,
            train_size=train_size,
            test_size=test_size,
            step_size=step_size,
        ):

            model = train_callback(
                train_df,
            )

            predictions = predict_callback(
                model,
                test_df,
            )

            actual = (
                test_df["target"]
                .tolist()
            )

            mae = MetricsEngine.mae(
                actual,
                predictions,
            )

            rmse = MetricsEngine.rmse(
                actual,
                predictions,
            )

            mape = MetricsEngine.mape(
                actual,
                predictions,
            )

            directional_accuracy = (
                MetricsEngine.directional_accuracy(
                    actual,
                    predictions,
                )
            )

            results.append(
                {
                    "train_rows": len(
                        train_df
                    ),

                    "test_rows": len(
                        test_df
                    ),

                    "mae": float(mae),

                    "rmse": float(rmse),

                    "mape": float(mape),

                    "directional_accuracy": float(
                        directional_accuracy
                    ),

                    "predictions": predictions,
                }
            )

        summary = {
            "mae": sum(
                r["mae"]
                for r in results
            )
            / len(results),

            "rmse": sum(
                r["rmse"]
                for r in results
            )
            / len(results),

            "mape": sum(
                r["mape"]
                for r in results
            )
            / len(results),

            "directional_accuracy": sum(
                r["directional_accuracy"]
                for r in results
            )
            / len(results),
        }

        return {
            "windows": len(results),
            "summary": summary,
            "results": results,
        }