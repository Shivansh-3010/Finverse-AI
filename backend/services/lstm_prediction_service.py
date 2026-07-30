import torch
import numpy as np
import pandas as pd

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)

from repositories.news_article_repository import (
    NewsArticleRepository,
)

from forecasting.dataset_builder import (
    DatasetBuilder,
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

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
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
            c
            for c in dataset.columns
            if c not in [
                "timestamp",
                "target",
            ]
        ]
        
        print("Feature count:", len(feature_columns))
        print("Feature columns:", feature_columns)

        feature_matrix = dataset[
            feature_columns
        ].values

        scaler = LSTMScalerManager.load(
            "models/lstm/lstm_scaler.pkl"
        )

        feature_matrix = scaler.transform(
            feature_matrix
        )

        sequence = feature_matrix[-30:]

        X_tensor = torch.tensor(
            sequence.reshape(
                1,
                30,
                len(feature_columns),
            ),
            dtype=torch.float32,
        )

        model = LSTMModelManager.load(
            LSTMEngine(
                input_size=len(feature_columns),
            ),
            "models/lstm/lstm_model.pt",
        )

        model.eval()

        with torch.no_grad():

            predicted_return_pct = (
                model(
                    X_tensor
                )
                .item()
            )
        
        current_price = float(
            ohlcv_df.iloc[-1]["close"]
        )

        prediction = current_price * (
            1
            + (
                predicted_return_pct
                / 100.0
            )
        )

        return {
            "symbol": symbol,
            "model": "lstm",
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
            "features": len(
                feature_columns
            ),
        }