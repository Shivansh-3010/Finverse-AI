import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

from forecasting.dataset_builder import DatasetBuilder
from forecasting.lstm_dataset_builder import LSTMDatasetBuilder
from forecasting.lstm_model_manager import LSTMModelManager
from forecasting.lstm_scaler_manager import LSTMScalerManager
from forecasting.lstm_trainer import LSTMTrainer

from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)
from repositories.news_article_repository import (
    NewsArticleRepository,
)
from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
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

        if not records:
            raise ValueError(
                f"No OHLCV history found for {symbol}"
            )

        ohlcv_df = ohlcv_to_dataframe(records)

        candlestick_records = (
            CandlestickPatternRepository(db)
            .get_history_by_timeframe(
                symbol=symbol,
                timeframe=timeframe,
            )
        )

        candlestick_df = pd.DataFrame(
            [
                {
                    "timestamp": p.timestamp,
                    "strength": p.strength,
                    "confidence": p.confidence,
                    "candlestick_score": p.candlestick_score,
                }
                for p in candlestick_records
            ]
        )

        news_articles = (
            NewsArticleRepository(db)
            .get_training_history(symbol)
        )

        dataset = DatasetBuilder.build(
            df=ohlcv_df,
            candlestick_features=candlestick_df,
            news_articles=news_articles,
        )

        feature_columns = [
            column
            for column in dataset.columns
            if column not in [
                "timestamp",
                "target",
            ]
        ]
        
        print("Feature count:", len(feature_columns))
        print("Feature columns:", feature_columns)

        X = dataset[
            feature_columns
        ].values

        y = dataset[
            "target"
        ].values

        scaler = MinMaxScaler()

        X = scaler.fit_transform(X)

        X, y = LSTMDatasetBuilder.build(
            dataset=dataset,
            sequence_length=30,
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
        
        print("Model saved successfully.")

        LSTMScalerManager.save(
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