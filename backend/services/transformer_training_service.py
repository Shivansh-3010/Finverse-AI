import numpy as np
import torch

from pathlib import Path

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)

from mlops.registry.model_registry import (
    ModelRegistry,
)

from forecasting.forecast_preprocessing_pipeline import (
    ForecastPreprocessingPipeline,
)

from forecasting.scaler_manager import (
    ScalerManager,
)

from forecasting.transformer_model_manager import (
    TransformerModelManager,
)

from forecasting.transformer_trainer import (
    TransformerTrainer,
)


class TransformerTrainingService:

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
            / "transformer"
        )

        model_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        model_path = (
            model_dir
            / f"{symbol.lower()}_transformer_{timeframe}.pt"
        )

        scaler_path = (
            model_dir
            / f"{symbol.lower()}_transformer_scaler_{timeframe}.pkl"
        )

        model = TransformerTrainer.train(
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
                    /
                    np.maximum(
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

        print(f"MAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"MAPE: {mape:.4f}")
        print(
            f"Directional Accuracy: "
            f"{directional_accuracy:.2f}%"
        )

        TransformerModelManager.save(
            model,
            str(model_path),
        )

        print(
            "Model saved successfully."
        )

        ScalerManager.save(
            scaler,
            str(scaler_path),
        )
        
        ModelRegistry.register(
            model_name="transformer",
            symbol=symbol,
            horizon=timeframe,
            version=f"{timeframe}-v1",
            artifact_path=str(model_path),
            metrics={
                "mae": float(mae),
                "rmse": float(rmse),
                "mape": float(mape),
                "directional_accuracy": float(
                    directional_accuracy
                ),
            },
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