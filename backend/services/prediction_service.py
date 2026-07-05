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

        prediction = PredictionAgent.predict(
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
        )

        comparison = ModelComparisonService.compare(
            db=db,
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
        )

        return {
            "summary": prediction,
            "models": comparison,
        }