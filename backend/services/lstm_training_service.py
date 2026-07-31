from forecasting.forecast_preprocessing_pipeline import (
    ForecastPreprocessingPipeline,
)

from forecasting.lstm_model_manager import (
    LSTMModelManager,
)

from forecasting.scaler_manager import (
    ScalerManager,
)

from forecasting.lstm_trainer import (
    LSTMTrainer,
)


class LSTMTrainingService:

    @staticmethod
    def train(
        db,
        symbol: str,
        timeframe: str = "1d",
    ):

        pipeline = (
            ForecastPreprocessingPipeline.prepare(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
            )
        )

        X = pipeline["X"]
        y = pipeline["y"]
        scaler = pipeline["scaler"]
        feature_columns = pipeline["feature_columns"]

        print(
            "Feature count:",
            len(feature_columns),
        )

        print(
            "Feature columns:",
            feature_columns,
        )

        print(
            f"Training samples: {len(X)}"
        )

        model = LSTMTrainer.train(
            X,
            y,
            epochs=20,
        )

        LSTMModelManager.save(
            model,
            "models/lstm/lstm_model.pt",
        )

        print(
            "Model saved successfully."
        )

        ScalerManager.save(
            scaler,
            "models/lstm/lstm_scaler.pkl",
        )

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "samples": len(X),
            "features": len(feature_columns),
            "status": "trained",
        }