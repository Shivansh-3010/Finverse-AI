from agents.prediction_agent.agent import PredictionAgent


class PredictionService:

    @staticmethod
    def generate(
        symbol: str,
        timeframe: str = "1d"
    ):

        return PredictionAgent.predict(
            symbol=symbol,
            timeframe=timeframe
        )