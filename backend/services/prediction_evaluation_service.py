from forecasting.evaluation_metrics_engine import (
    EvaluationMetricsEngine,
)

from forecasting.model_leaderboard_engine import (
    ModelLeaderboardEngine,
)

from repositories.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)


class PredictionEvaluationService:

    @staticmethod
    def _metrics(
        evaluations,
    ):

        if not evaluations:
            return {}

        return {

            "total_predictions": len(
                evaluations
            ),

            "mae": round(
                EvaluationMetricsEngine.mae(
                    evaluations
                ),
                4,
            ),

            "rmse": round(
                EvaluationMetricsEngine.rmse(
                    evaluations
                ),
                4,
            ),

            "mape": round(
                EvaluationMetricsEngine.mape(
                    evaluations
                ),
                4,
            ),

            "directional_accuracy": round(
                EvaluationMetricsEngine.directional_accuracy(
                    evaluations
                ),
                2,
            ),

            "hit_rate": round(
                EvaluationMetricsEngine.hit_rate(
                    evaluations
                ),
                2,
            ),

            "mean_bias": round(
                EvaluationMetricsEngine.mean_bias(
                    evaluations
                ),
                4,
            ),

            "max_absolute_error": round(
                EvaluationMetricsEngine.max_absolute_error(
                    evaluations
                ),
                4,
            ),
        }

    @staticmethod
    def summary(
        db,
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        repository = (
            PredictionEvaluationRepository(
                db
            )
        )

        evaluations = (
            repository.get_history(
                symbol=symbol,
                timeframe=timeframe,
                horizon=horizon,
            )
        )

        if not evaluations:

            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "horizon": horizon,
                "overall": {},
                "rolling": {},
                "models": {},
                "leaderboard": [],
            }

        overall = (
            PredictionEvaluationService._metrics(
                evaluations
            )
        )

        rolling = {}

        for window in (
            30,
            90,
            180,
        ):

            recent = (
                repository.get_recent_history(
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                    limit=window,
                )
            )

            rolling[
                str(window)
            ] = (
                PredictionEvaluationService._metrics(
                    recent
                )
            )

        model_histories = {}

        model_reports = {}

        for model in (
            repository.get_available_models(
                symbol=symbol,
                timeframe=timeframe,
                horizon=horizon,
            )
        ):

            history = (
                repository.get_history_by_model(
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                    model_name=model,
                )
            )

            model_histories[
                model
            ] = history

            model_reports[
                model
            ] = (
                PredictionEvaluationService._metrics(
                    history
                )
            )

        leaderboard = (
            ModelLeaderboardEngine.rank(
                model_histories
            )
        )

        return {

            "symbol": symbol,

            "timeframe": timeframe,
            
            "horizon": horizon,

            "overall": overall,

            "rolling": rolling,

            "models": model_reports,

            "leaderboard": leaderboard,
        }