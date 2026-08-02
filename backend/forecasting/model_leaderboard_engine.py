from forecasting.evaluation_metrics_engine import (
    EvaluationMetricsEngine,
)


class ModelLeaderboardEngine:

    @staticmethod
    def rank(
        model_histories: dict,
    ):

        leaderboard = []

        for model_name, evaluations in (
            model_histories.items()
        ):

            if not evaluations:
                continue

            leaderboard.append(
                {
                    "model": model_name,

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
                        EvaluationMetricsEngine.directional_accuracy(
                            evaluations
                        ),

                    "hit_rate":
                        EvaluationMetricsEngine.hit_rate(
                            evaluations
                        ),
                }
            )

        leaderboard.sort(
            key=lambda x: (
                x["mae"],
                -x["directional_accuracy"],
                -x["hit_rate"],
            )
        )

        for rank, model in enumerate(
            leaderboard,
            start=1,
        ):
            model["rank"] = rank

        return leaderboard