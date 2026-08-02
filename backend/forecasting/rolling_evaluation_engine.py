from forecasting.evaluation_metrics_engine import (
    EvaluationMetricsEngine,
)


class RollingEvaluationEngine:

    DEFAULT_WINDOWS = (
        20,
        50,
        100,
        250,
    )

    @staticmethod
    def evaluate(
        evaluations,
        windows=None,
    ):

        if windows is None:
            windows = (
                RollingEvaluationEngine
                .DEFAULT_WINDOWS
            )

        results = {}

        for window in windows:

            subset = evaluations[-window:]

            if not subset:
                continue

            results[window] = {

                "sample_size": len(
                    subset
                ),

                "mae":
                    EvaluationMetricsEngine.mae(
                        subset
                    ),

                "rmse":
                    EvaluationMetricsEngine.rmse(
                        subset
                    ),

                "mape":
                    EvaluationMetricsEngine.mape(
                        subset
                    ),

                "smape":
                    EvaluationMetricsEngine.smape(
                        subset
                    ),

                "directional_accuracy":
                    EvaluationMetricsEngine.directional_accuracy(
                        subset
                    ),

                "hit_rate":
                    EvaluationMetricsEngine.hit_rate(
                        subset
                    ),

                "mean_bias":
                    EvaluationMetricsEngine.mean_bias(
                        subset
                    ),

                "max_absolute_error":
                    EvaluationMetricsEngine.max_absolute_error(
                        subset
                    ),
            }

        return results