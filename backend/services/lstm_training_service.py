import numpy as np
import torch

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)

from pathlib import Path

from mlops.registry.model_registry import (
    ModelRegistry,
)

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
        
        model_dir = (
            Path("models")
            / "lstm"
        )

        model_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        model_path = (
            model_dir
            / f"{symbol.lower()}_lstm_{timeframe}.pt"
        )

        scaler_path = (
            model_dir
            / f"{symbol.lower()}_lstm_scaler_{timeframe}.pkl"
        )

        model = LSTMTrainer.train(
            X,
            y,
            epochs=20,
        )
        
        model.eval()

        with torch.no_grad():

            predictions = (
                model(
                    torch.tensor(
                        X,
                        dtype=torch.float32,
                    )
                )
                .cpu()
                .numpy()
                .flatten()
            )

        mae = mean_absolute_error(
            y,
            predictions,
        )

        rmse = np.sqrt(
            mean_squared_error(
                y,
                predictions,
            )
        )

        mape = (
            np.mean(
                np.abs(
                    (y - predictions)
                    / np.maximum(
                        np.abs(y),
                        1e-6,
                    )
                )
            )
            * 100
        )

        directional_accuracy = (
            (
                np.sign(predictions)
                ==
                np.sign(y)
            ).mean()
            * 100
        )

        print()

        print(
            f"MAE: {mae:.4f}"
        )

        print(
            f"RMSE: {rmse:.4f}"
        )

        print(
            f"MAPE: {mape:.4f}"
        )

        print(
            f"Directional Accuracy: {directional_accuracy:.2f}%"
        )

        LSTMModelManager.save(
            model,
            str(model_path),
        )
        
        ModelRegistry.register(
            model_name="lstm",
            symbol=symbol,
            horizon=timeframe,
            version=f"{timeframe}-v1",
            artifact_path=(
                f"models/lstm/"
                f"{symbol.lower()}_lstm_{timeframe}.pt"
            ),
            metrics={
                "mae": float(mae),
                "rmse": float(rmse),
                "mape": float(mape),
                "directional_accuracy": float(
                    directional_accuracy
                ),
            },
        )

        print(
            "Model saved successfully."
        )

        ScalerManager.save(
            scaler,
            str(scaler_path),
        )

        return {

            "symbol": symbol,

            "timeframe": timeframe,

            "samples": len(X),

            "features": len(feature_columns),

            "mae": float(mae),

            "rmse": float(rmse),

            "mape": float(mape),

            "directional_accuracy": float(
                directional_accuracy
            ),

            "status": "trained",
        }