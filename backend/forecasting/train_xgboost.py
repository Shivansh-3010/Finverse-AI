import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(
        str(PROJECT_ROOT)
    )
import pandas as pd
import joblib
from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

from forecasting.dataset_builder import (
    DatasetBuilder,
)

from forecasting.xgboost_engine import (
    XGBoostEngine,
)
from sklearn.model_selection import (
    train_test_split,
)
from forecasting.metrics_engine import (
    MetricsEngine,
)
from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)
from repositories.news_article_repository import (
    NewsArticleRepository,
)

from forecasting.news_feature_builder import (
    NewsFeatureBuilder,
)

def train():

    db = SessionLocal()

    try:

        records = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe(
                symbol="RELIANCE",
                timeframe="1d"
            )
        )
        
        patterns = (
            CandlestickPatternRepository(db)
            .get_history_by_timeframe(
                "RELIANCE",
                "1d"
            )
        )
        
        news_articles = (
            NewsArticleRepository(db)
            .get_history(
                "RELIANCE"
            )
        )

        news_features = (
            NewsFeatureBuilder.build(
                news_articles
            )
        )

        df = ohlcv_to_dataframe(
            records
        )
        
        candlestick_features = pd.DataFrame([
            {
                "timestamp": p.timestamp,
                "strength": p.strength,
                "confidence": p.confidence,
                "candlestick_score": p.candlestick_score,
            }
            for p in patterns
        ])

        dataset = DatasetBuilder.build(
            df,
            candlestick_features
        )
        
        if not news_features.empty:

            dataset["date"] = (
                dataset["timestamp"]
                .dt.date
            )

            dataset = dataset.merge(
                news_features,
                on="date",
                how="left"
            )
            
            print(
                dataset[
                    [
                        "date",
                        "avg_news_score",
                        "article_count",
                        "positive_count",
                        "negative_count",
                    ]
                ]
                .tail(20)
            )

            dataset[
                "avg_news_score"
            ] = (
                dataset[
                    "avg_news_score"
                ]
                .fillna(0)
            )

            dataset[
                "avg_news_confidence"
            ] = (
                dataset[
                    "avg_news_confidence"
                ]
                .fillna(0)
            )

        X = dataset[
            [
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
            ]
        ]

        y = dataset["target"]

        model = (
            XGBoostEngine.build_model()
        )

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.2,
                shuffle=False
            )
        )

        model.fit(
            X_train,
            y_train
        )
        
        Path(
            "models/xgboost"
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        joblib.dump(
            model,
            "models/xgboost/reliance_xgb.pkl"
        )

        joblib.dump(
            list(X.columns),
            "models/xgboost/reliance_xgb_features.pkl"
        )

        predictions = model.predict(
            X_test
        )
        
        mae = MetricsEngine.mae(
            y_test,
            predictions
        )

        rmse = MetricsEngine.rmse(
            y_test,
            predictions
        )

        mape = MetricsEngine.mape(
            y_test,
            predictions
        )

        directional_accuracy = (
            MetricsEngine.directional_accuracy(
                y_test.values,
                predictions
            )
        )

        print(
            "Training complete"
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
            round(mae, 4)
        )

        print(
            "RMSE:",
            round(rmse, 4)
        )

        print(
            "MAPE:",
            round(mape, 4)
        )

        print(
            "Directional Accuracy:",
            round(
                directional_accuracy,
                2
            ),
            "%"
        )
        
        print("\nFeature Importance")

        importance = model.feature_importances_

        for feature, score in sorted(
            zip(X.columns, importance),
            key=lambda x: x[1],
            reverse=True
        ):
            print(
                f"{feature}: {score:.4f}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    train()