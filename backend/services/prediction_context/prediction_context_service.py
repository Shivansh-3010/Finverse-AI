from database.session import SessionLocal

from agents.prediction_agent.agent import (
    PredictionAgent,
)

from services.model_comparison_service import (
    ModelComparisonService,
)

from services.prediction_evaluation_service import (
    PredictionEvaluationService,
)

from services.model_leaderboard_service import (
    ModelLeaderboardService,
)

from feature_store.prediction.prediction_features import (
    PredictionFeatureStore,
)


class PredictionContextService:

    @staticmethod
    def build(
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        db = SessionLocal()

        try:

            prediction = (
                PredictionAgent.predict(
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                )
            )

            comparison = (
                ModelComparisonService.compare(
                    db=db,
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                )
            )

            evaluation = (
                PredictionEvaluationService.summary(
                    db=db,
                    symbol=symbol,
                    timeframe=timeframe,
                )
            )

            leaderboard = (
                ModelLeaderboardService.leaderboard(
                    db=db,
                    symbol=symbol,
                    timeframe=timeframe,
                )
            )

            feature_store = (
                PredictionFeatureStore.latest(
                    db=db,
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                )
            )

            return {

                "prediction": prediction,

                "feature_store": feature_store,

                "comparison": comparison,

                "evaluation": evaluation,

                "leaderboard": leaderboard,
            }

        finally:

            db.close()