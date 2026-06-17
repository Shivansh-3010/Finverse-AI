import numpy as np

from sklearn.preprocessing import (
    MinMaxScaler,
)

from forecasting.lstm_scaler_manager import (
    LSTMScalerManager,
)

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from forecasting.lstm_dataset_builder import (
    LSTMDatasetBuilder,
)

from forecasting.lstm_trainer import (
    LSTMTrainer,
)

from forecasting.lstm_model_manager import (
    LSTMModelManager,
)


class LSTMTrainingService:

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
                np.array(prices).reshape(-1, 1)
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
            LSTMTrainer.train(
                X,
                y,
                epochs=20,
            )
        )

        LSTMModelManager.save(
            model,
            "models/lstm/lstm_model.pt",
        )
        
        LSTMScalerManager.save(
            scaler,
            "models/lstm/lstm_scaler.pkl",
        )

        return {
            "symbol": symbol,
            "samples": len(X),
            "status": "trained",
        }