import pandas as pd

from sklearn.preprocessing import MinMaxScaler

from forecasting.dataset_builder import DatasetBuilder
from forecasting.lstm_dataset_builder import LSTMDatasetBuilder

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


class ForecastPreprocessingPipeline:

    @staticmethod
    def prepare(
        db,
        symbol: str,
        timeframe: str = "1d",
        sequence_length: int = 30,
        build_sequences: bool = True,
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

        scaler = MinMaxScaler()

        dataset[feature_columns] = scaler.fit_transform(
            dataset[feature_columns]
        )

        result = {
            "dataset": dataset,
            "scaler": scaler,
            "feature_columns": feature_columns,
            "ohlcv_df": ohlcv_df,
        }

        if build_sequences:

            X, y = LSTMDatasetBuilder.build(
                dataset=dataset,
                sequence_length=sequence_length,
            )

            result["X"] = X
            result["y"] = y

        return result