import numpy as np
import torch

from forecasting.forecast_preprocessing_pipeline import (
    ForecastPreprocessingPipeline,
)

from forecasting.transformer_engine import (
    TransformerEngine,
)

from forecasting.transformer_model_manager import (
    TransformerModelManager,
)

from forecasting.scaler_manager import (
    ScalerManager,
)


class TransformerPredictionService:

    @staticmethod
    def predict(
        db,
        symbol: str,
        timeframe: str = "1d",
    ):

        pipeline = (
            ForecastPreprocessingPipeline.prepare(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
                build_sequences=False,
            )
        )

        dataset = pipeline["dataset"]
        feature_columns = pipeline["feature_columns"]
        ohlcv_df = pipeline["ohlcv_df"]

        print(
            "Feature count:",
            len(feature_columns),
        )

        print(
            "Feature columns:",
            feature_columns,
        )

        scaler = ScalerManager.load(
            "models/transformer/transformer_scaler.pkl",
        )

        dataset[feature_columns] = scaler.transform(
            dataset[feature_columns]
        )

        sequence = (
            dataset[feature_columns]
            .tail(30)
            .to_numpy(dtype=np.float32)
        )

        X_tensor = torch.tensor(
            sequence,
            dtype=torch.float32,
        ).unsqueeze(0)

        model = TransformerModelManager.load(
            TransformerEngine(
                input_size=len(feature_columns),
            ),
            "models/transformer/transformer_model.pt",
        )

        with torch.no_grad():

            predicted_return_pct = (
                model(X_tensor)
                .item()
            )

        current_price = float(
            ohlcv_df.iloc[-1]["close"]
        )

        prediction = current_price * (
            1
            + predicted_return_pct / 100.0
        )
        
        confidence = max(
            0.0,
            min(
                100.0,
                100.0
                - min(
                    abs(
                        predicted_return_pct
                    ) * 10.0,
                    50.0,
                ),
            ),
        )

        return {
            "symbol": symbol,
            "model": "transformer",
            "timeframe": timeframe,

            "current_price": round(
                current_price,
                2,
            ),

            "prediction": round(
                prediction,
                2,
            ),

            "predicted_return_pct": round(
                predicted_return_pct,
                4,
            ),

            "direction": (
                "bullish"
                if predicted_return_pct > 0
                else "bearish"
            ),

            "confidence": round(
                confidence,
                2,
            ),

            "features": len(
                feature_columns
            ),
        }