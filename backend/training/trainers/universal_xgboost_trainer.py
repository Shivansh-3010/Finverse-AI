from pathlib import Path

import joblib
import pandas as pd

from database.session import SessionLocal

from forecasting.dataset_builder import (
    DatasetBuilder,
)

from forecasting.horizons import (
    HORIZON_DAYS,
)

from forecasting.metrics_engine import (
    MetricsEngine,
)

from forecasting.news_feature_builder import (
    NewsFeatureBuilder,
)

from forecasting.xgboost_engine import (
    XGBoostEngine,
)

from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)

from repositories.news_article_repository import (
    NewsArticleRepository,
)

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from training.universe.universe_selector import (
    UniverseSelector,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

from sklearn.model_selection import (
    train_test_split,
)


FEATURE_COLUMNS = [
    "rsi",
    "macd",
    "macd_signal",
    "atr",
    "adx",
    "mfi",
    "obv",
    "vwap",
    "bb_upper",
    "bb_middle",
    "bb_lower",
    "strength",
    "confidence",
    "candlestick_score",
    "avg_news_score",
    "avg_news_confidence",
    "article_count",
    "recent_article_count",
    "positive_count",
    "negative_count",
    "neutral_count",
    "symbol_id",
]


class UniversalXGBoostTrainer:

    @staticmethod
    def train(
        horizon: str = "1d",
        max_symbols: int = 50,
    ):

        if horizon not in HORIZON_DAYS:

            raise ValueError(
                f"Unsupported horizon: {horizon}"
            )

        db = SessionLocal()

        try:

            symbols = (
                UniverseSelector.get_symbols(
                    db=db,
                    timeframe="1d",
                    min_candles=5000,
                )
            )[:max_symbols]

            datasets = []

            for index, symbol in enumerate(symbols):

                print(
                    f"[{index + 1}/{len(symbols)}] {symbol}"
                )

                try:

                    records = (
                        OHLCVRepository(db)
                        .get_history_by_symbol_and_timeframe(
                            symbol=symbol,
                            timeframe="1d",
                        )
                    )

                    if len(records) < 200:
                        continue

                    patterns = (
                        CandlestickPatternRepository(db)
                        .get_history_by_timeframe(
                            symbol,
                            "1d",
                        )
                    )

                    news_articles = (
                        NewsArticleRepository(db)
                        .get_training_history(symbol)
                    )

                    news_features = (
                        NewsFeatureBuilder.build(
                            news_articles
                        )
                    )

                    df = ohlcv_to_dataframe(
                        records
                    )

                    candlestick_features = pd.DataFrame(
                        [
                            {
                                "timestamp": p.timestamp,
                                "strength": p.strength,
                                "confidence": p.confidence,
                                "candlestick_score": p.candlestick_score,
                            }
                            for p in patterns
                        ]
                    )

                    dataset = DatasetBuilder.build(
                        df,
                        candlestick_features,
                        horizon_days=
                            HORIZON_DAYS[horizon],
                    )
                    
                    dataset["symbol_id"] = index

                    if not news_features.empty:

                        dataset["date"] = (
                            dataset["timestamp"]
                            .dt.date
                        )

                        dataset = dataset.merge(
                            news_features,
                            on="date",
                            how="left",
                        )

                    for column in [
                        "avg_news_score",
                        "avg_news_confidence",
                        "article_count",
                        "recent_article_count",
                        "positive_count",
                        "negative_count",
                        "neutral_count",
                    ]:

                        if column not in dataset.columns:
                            dataset[column] = 0

                        dataset[column] = (
                            dataset[column]
                            .fillna(0)
                        )

                    datasets.append(
                        dataset
                    )

                except Exception as e:

                    print(
                        f"Skipped {symbol}: {e}"
                    )

            combined_dataset = pd.concat(
                datasets,
                ignore_index=True,
            )

            X = combined_dataset[
                FEATURE_COLUMNS
            ]

            y = combined_dataset[
                "target"
            ]

            X_train, X_test, y_train, y_test = (
                train_test_split(
                    X,
                    y,
                    test_size=0.2,
                    shuffle=False,
                )
            )

            model = (
                XGBoostEngine.build_model()
            )

            model.fit(
                X_train,
                y_train,
            )

            Path(
                "models/xgboost"
            ).mkdir(
                parents=True,
                exist_ok=True,
            )

            joblib.dump(
                model,
                f"models/xgboost/universal_xgb_{horizon}.pkl",
            )

            joblib.dump(
                FEATURE_COLUMNS,
                f"models/xgboost/universal_xgb_features_{horizon}.pkl",
            )

            predictions = model.predict(
                X_test
            )

            print(
                "\nTraining Complete"
            )

            print(
                "Train Rows:",
                len(X_train)
            )

            print(
                "Test Rows:",
                len(X_test)
            )

            print(
                "MAE:",
                round(
                    MetricsEngine.mae(
                        y_test,
                        predictions,
                    ),
                    4,
                )
            )

            print(
                "RMSE:",
                round(
                    MetricsEngine.rmse(
                        y_test,
                        predictions,
                    ),
                    4,
                )
            )

            print(
                "MAPE:",
                round(
                    MetricsEngine.mape(
                        y_test,
                        predictions,
                    ),
                    4,
                )
            )

            print(
                "Directional Accuracy:",
                round(
                    MetricsEngine.directional_accuracy(
                        y_test.values,
                        predictions,
                    ),
                    2,
                ),
                "%",
            )

        finally:
            db.close()