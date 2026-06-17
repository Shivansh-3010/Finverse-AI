import torch
import numpy as np

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from forecasting.transformer_engine import (
    TransformerEngine,
)

from forecasting.transformer_model_manager import (
    TransformerModelManager,
)

from forecasting.lstm_scaler_manager import (
    LSTMScalerManager,
)


class TransformerPredictionService:

    @staticmethod
    def predict(
        db,
        symbol: str,
        timeframe: str = "1d",
    ):

        records = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe(
                symbol=symbol,
                timeframe=timeframe,
            )
        )

        prices = [
            record.close
            for record in records
            if record.close is not None
            and not np.isnan(
                record.close
            )
        ]

        scaler = (
            LSTMScalerManager.load(
                "models/transformer/transformer_scaler.pkl"
            )
        )

        prices_scaled = (
            scaler.transform(
                np.array(prices).reshape(
                    -1,
                    1
                )
            )
            .flatten()
        )

        sequence = prices_scaled[-30:]

        X = np.array(
            sequence
        ).reshape(
            1,
            30,
            1
        )

        X_tensor = torch.tensor(
            X,
            dtype=torch.float32,
        )

        model = (
            TransformerModelManager.load(
                TransformerEngine(),
                "models/transformer/transformer_model.pt",
            )
        )

        with torch.no_grad():

            prediction_scaled = (
                model(
                    X_tensor
                )
                .item()
            )

        prediction = (
            scaler.inverse_transform(
                np.array(
                    [[prediction_scaled]]
                )
            )[0][0]
        )

        current_price = (
            prices[-1]
        )

        predicted_return_pct = (
            (
                prediction
                - current_price
            )
            / current_price
        ) * 100

        return {
            "symbol": symbol,
            "model": "transformer",

            "prediction":
                round(
                    float(prediction),
                    2
                ),

            "predicted_return_pct":
                round(
                    float(
                        predicted_return_pct
                    ),
                    4
                ),

            "direction":
                (
                    "bullish"
                    if predicted_return_pct > 0
                    else "bearish"
                ),
        }