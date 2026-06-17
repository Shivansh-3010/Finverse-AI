import torch
import numpy as np

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from forecasting.lstm_engine import (
    LSTMEngine,
)

from forecasting.lstm_model_manager import (
    LSTMModelManager,
)

from forecasting.lstm_scaler_manager import (
    LSTMScalerManager,
)


class LSTMPredictionService:

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
                "models/lstm/lstm_scaler.pkl"
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
            LSTMModelManager.load(
                LSTMEngine(),
                "models/lstm/lstm_model.pt",
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
        
        print(
            "Current Price:",
            current_price
        )

        print(
            "Predicted Price:",
            prediction
        )

        return {
            "symbol": symbol,

            "model": "lstm",

            "prediction":
                round(
                    prediction,
                    2
                ),

            "predicted_return_pct":
                round(
                    predicted_return_pct,
                    4
                ),

            "direction":
                (
                    "bullish"
                    if predicted_return_pct > 0
                    else "bearish"
                ),
        }