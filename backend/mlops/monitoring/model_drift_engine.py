from forecasting.evaluation_metrics_engine import (
    EvaluationMetricsEngine,
)


class ModelDriftEngine:

    MIN_EVALUATIONS = 10

    ERROR_METRICS = {
        "mae",
        "rmse",
        "mape",
    }

    @staticmethod
    def calculate(
        historical_evaluations,
        recent_evaluations,
    ):
        """
        Compare historical and recent model
        performance to detect performance degradation.
        """

        if (
            len(historical_evaluations)
            < ModelDriftEngine.MIN_EVALUATIONS
            or
            len(recent_evaluations)
            < ModelDriftEngine.MIN_EVALUATIONS
        ):
            return {
                "status": "insufficient_data",
                "drift_detected": False,
                "drift_score": 0.0,
                "severity": "UNKNOWN",
                "required_evaluations":
                    ModelDriftEngine.MIN_EVALUATIONS,
                "historical_evaluations":
                    len(historical_evaluations),
                "recent_evaluations":
                    len(recent_evaluations),
                "metrics": {},
            }

        historical_metrics = (
            ModelDriftEngine
            ._calculate_metrics(
                historical_evaluations
            )
        )

        recent_metrics = (
            ModelDriftEngine
            ._calculate_metrics(
                recent_evaluations
            )
        )

        metric_report = {}

        degraded_metrics = 0

        for metric in historical_metrics:

            historical_value = float(
                historical_metrics[metric]
            )

            recent_value = float(
                recent_metrics[metric]
            )

            absolute_change = abs(
                recent_value
                - historical_value
            )

            if abs(historical_value) > 1e-12:

                relative_change_pct = (
                    absolute_change
                    / abs(historical_value)
                ) * 100

            else:

                relative_change_pct = (
                    100.0
                    if absolute_change > 0
                    else 0.0
                )

            if metric in (
                ModelDriftEngine.ERROR_METRICS
            ):

                degraded = (
                    recent_value
                    > historical_value
                )

            elif metric == "directional_accuracy":

                degraded = (
                    recent_value
                    < historical_value
                )

            elif metric == "mean_bias":

                degraded = (
                    abs(recent_value)
                    > abs(historical_value)
                )

            else:

                degraded = False

            if degraded:
                degraded_metrics += 1

            metric_report[metric] = {

                "historical_value":
                    round(
                        historical_value,
                        6,
                    ),

                "recent_value":
                    round(
                        recent_value,
                        6,
                    ),

                "absolute_change":
                    round(
                        absolute_change,
                        6,
                    ),

                "relative_change_pct":
                    round(
                        relative_change_pct,
                        4,
                    ),

                "degraded": degraded,
            }

        drift_score = (
            degraded_metrics
            / len(metric_report)
        )

        drift_detected = (
            degraded_metrics >= 2
        )

        if not drift_detected:

            severity = "LOW"

        elif drift_score < 0.75:

            severity = "MEDIUM"

        elif drift_score < 1.0:

            severity = "HIGH"

        else:

            severity = "CRITICAL"

        return {

            "status": "evaluated",

            "drift_detected":
                drift_detected,

            "drift_score":
                round(
                    drift_score,
                    4,
                ),

            "severity":
                severity,

            "required_evaluations":
                ModelDriftEngine
                .MIN_EVALUATIONS,

            "historical_evaluations":
                len(historical_evaluations),

            "recent_evaluations":
                len(recent_evaluations),

            "metrics":
                metric_report,
        }

    @staticmethod
    def _calculate_metrics(
        evaluations,
    ):

        return {

            "mae":
                EvaluationMetricsEngine.mae(
                    evaluations
                ),

            "rmse":
                EvaluationMetricsEngine.rmse(
                    evaluations
                ),

            "mape":
                EvaluationMetricsEngine.mape(
                    evaluations
                ),

            "directional_accuracy":
                EvaluationMetricsEngine
                .directional_accuracy(
                    evaluations
                ),

            "mean_bias":
                EvaluationMetricsEngine.mean_bias(
                    evaluations
                ),
        }