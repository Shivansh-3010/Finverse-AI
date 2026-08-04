from agents.prediction_agent.agent import PredictionAgent


class PredictionService:

    @staticmethod
    def generate(
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        return PredictionAgent.predict(
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
        )

    @staticmethod
    def generate_report(
        db,
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        from services.model_comparison_service import (
            ModelComparisonService,
        )

        from services.ensemble_forecast_service import (
            EnsembleForecastService,
        )

        from services.prediction_evaluation_service import (
            PredictionEvaluationService,
        )

        from services.model_leaderboard_service import (
            ModelLeaderboardService,
        )

        prediction = PredictionAgent.predict(
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
        )

        comparison = (
            ModelComparisonService.compare(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
                horizon=horizon,
            )
        )

        ensemble = (
            EnsembleForecastService.forecast(
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

        return {

            "prediction": prediction,

            "ensemble": ensemble,

            "model_comparison": comparison,

            "evaluation": evaluation,

            "leaderboard": leaderboard,
        }