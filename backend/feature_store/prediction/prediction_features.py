from repositories.prediction_repository import (
    PredictionRepository,
)


class PredictionFeatureStore:

    @staticmethod
    def latest(
        db,
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        repository = PredictionRepository(db)

        predictions = repository.get_latest_predictions(
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
        )

        if not predictions:
            return {}

        average_prediction = (
            sum(
                p.prediction
                for p in predictions
            )
            / len(predictions)
        )

        average_confidence = (
            sum(
                p.confidence
                for p in predictions
            )
            / len(predictions)
        )

        bullish = sum(
            1
            for p in predictions
            if p.prediction > 0
        )

        bearish = sum(
            1
            for p in predictions
            if p.prediction < 0
        )

        return {

            "symbol": symbol,

            "timeframe": timeframe,

            "horizon": horizon,

            "prediction": average_prediction,

            "confidence": average_confidence,

            "bullish_models": bullish,

            "bearish_models": bearish,

            "model_count": len(predictions),

            "agreement": (
                max(
                    bullish,
                    bearish,
                )
                / len(predictions)
            )
            * 100,
        }