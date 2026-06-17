import numpy as np

from sklearn.preprocessing import (
    MinMaxScaler,
)

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from forecasting.lstm_dataset_builder import (
    LSTMDatasetBuilder,
)

from forecasting.lstm_scaler_manager import (
    LSTMScalerManager,
)

from forecasting.transformer_trainer import (
    TransformerTrainer,
)

from forecasting.transformer_model_manager import (
    TransformerModelManager,
)


class TransformerTrainingService:

    @staticmethod
    def train(
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

        print(
            "Valid Prices:",
            len(prices)
        )

        scaler = MinMaxScaler()

        prices = (
            scaler.fit_transform(
                np.array(prices).reshape(
                    -1,
                    1
                )
            )
            .flatten()
        )

        X, y = (
            LSTMDatasetBuilder.build(
                prices=prices,
                sequence_length=30,
            )
        )

        model = (
            TransformerTrainer.train(
                X,
                y,
                epochs=20,
            )
        )

        TransformerModelManager.save(
            model,
            "models/transformer/transformer_model.pt",
        )

        LSTMScalerManager.save(
            scaler,
            "models/transformer/transformer_scaler.pkl",
        )

        return {
            "symbol": symbol,
            "samples": len(X),
            "status": "trained",
        }