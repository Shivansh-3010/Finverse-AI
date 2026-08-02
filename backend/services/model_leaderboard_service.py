from forecasting.model_leaderboard_engine import (
    ModelLeaderboardEngine,
)

from repositories.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)


class ModelLeaderboardService:

    MODELS = (
        "xgboost",
        "prophet",
        "lstm",
        "transformer",
    )

    @staticmethod
    def leaderboard(
        db,
        symbol: str,
        timeframe: str = "1d",
        window: int = 100,
    ):

        repository = (
            PredictionEvaluationRepository(
                db
            )
        )

        histories = {}

        for model in (
            ModelLeaderboardService.MODELS
        ):

            histories[model] = (
                repository.get_recent_history(
                    symbol=symbol,
                    timeframe=timeframe,
                    model_name=model,
                    limit=window,
                )
            )

        return (
            ModelLeaderboardEngine.rank(
                histories
            )
        )