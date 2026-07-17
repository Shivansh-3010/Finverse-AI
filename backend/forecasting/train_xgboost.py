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

from repositories.risk_metric_repository import (
    RiskMetricRepository,
)

from repositories.support_resistance_repository import (
    SupportResistanceRepository,
)

from forecasting.news_feature_builder import (
    NewsFeatureBuilder,
)
from forecasting.horizons import (
    HORIZON_DAYS,
)

def train(
    symbol: str = "RELIANCE",
    horizon: str = "1d",
):
    if horizon not in HORIZON_DAYS:

        raise ValueError(
            f"Unsupported horizon: {horizon}"
        )

    db = SessionLocal()

    try:

        records = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe(
                symbol=symbol,
                timeframe="1d"
            )
        )
        
        patterns = (
            CandlestickPatternRepository(db)
            .get_history_by_timeframe(
                symbol=symbol,
                timeframe="1d",
            )
        )
        
        news_articles = (
            NewsArticleRepository(db)
            .get_training_history(
                symbol=symbol,
            )
        )
        
        risk_history = (
            RiskMetricRepository(db)
            .get_history(
                symbol=symbol,
                timeframe="1d",
            )
        )

        sr_history = (
            SupportResistanceRepository(db)
            .get_history_by_timeframe(
                symbol=symbol,
                timeframe="1d",
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
        
        risk_df = pd.DataFrame([
            {
                "timestamp": r.timestamp,
                "volatility_252d": r.volatility_252d,
                "drawdown_252d": r.drawdown_252d,
                "var95_252d": r.var95_252d,
                "expected_shortfall_252d": r.expected_shortfall_252d,
                "risk_score": r.risk_score,
            }
            for r in risk_history
        ])

        signal_map = {
            "support": 1.0,
            "resistance": -1.0,
            "breakout": 2.0,
            "breakdown": -2.0,
        }

        sr_df = pd.DataFrame([
            {
                "timestamp": s.timestamp,
                "nearest_support": s.nearest_support,
                "nearest_resistance": s.nearest_resistance,
                "support_strength": s.support_strength,
                "resistance_strength": s.resistance_strength,
                "distance_to_support_pct": s.distance_to_support_pct,
                "distance_to_resistance_pct": s.distance_to_resistance_pct,
                "breakout_zone_lower": s.breakout_zone_lower,
                "breakout_zone_upper": s.breakout_zone_upper,
                "breakdown_zone_lower": s.breakdown_zone_lower,
                "breakdown_zone_upper": s.breakdown_zone_upper,
                "signal_level": s.signal_level,
                "signal_value": signal_map.get(
                    s.signal,
                    0.0,
                ),
            }
            for s in sr_history
        ])

        dataset = DatasetBuilder.build(
            df,
            candlestick_features,
            horizon_days=
                HORIZON_DAYS[horizon],
        )
        
        if not risk_df.empty:

            dataset = dataset.merge(
                risk_df,
                on="timestamp",
                how="left",
            )

        if not sr_df.empty:

            dataset = dataset.merge(
                sr_df,
                on="timestamp",
                how="left",
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
            
        risk_columns = [
            "volatility_252d",
            "drawdown_252d",
            "var95_252d",
            "expected_shortfall_252d",
            "risk_score",
        ]

        sr_columns = [
            "nearest_support",
            "nearest_resistance",
            "support_strength",
            "resistance_strength",
            "distance_to_support_pct",
            "distance_to_resistance_pct",
            "breakout_zone_lower",
            "breakout_zone_upper",
            "breakdown_zone_lower",
            "breakdown_zone_upper",
            "signal_level",
            "signal_value",
        ]
        
        # Fill missing values

        for column in risk_columns + sr_columns:

            if column in dataset.columns:
                dataset[column] = (
                    dataset[column]
                    .fillna(0.0)
                )

        # --------------------------------------------------
        # DATA COVERAGE SUMMARY
        # --------------------------------------------------

        print("\n" + "=" * 60)
        print("FEATURE COVERAGE SUMMARY")
        print("=" * 60)

        columns_to_check = [
            "avg_news_score",
            "article_count",
            "nearest_support",
            "nearest_resistance",
            "signal_value",
        ]

        for col in columns_to_check:

            if col not in dataset.columns:
                continue

            non_zero = (
                dataset[col]
                .fillna(0)
                .ne(0)
                .sum()
            )

            print(
                f"{col}: "
                f"{non_zero}/{len(dataset)} "
                f"({100 * non_zero / len(dataset):.2f}%)"
            )

        X = dataset[
            [
                # Technical

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

                # Candlestick

                "strength",
                "confidence",
                "candlestick_score",

                # News

                "avg_news_score",
                "avg_news_confidence",
                "article_count",
                "recent_article_count",
                "positive_count",
                "negative_count",
                "neutral_count",

                # Risk

                "volatility_252d",
                "drawdown_252d",
                "var95_252d",
                "expected_shortfall_252d",
                "risk_score",

                # Support & Resistance

                "nearest_support",
                "nearest_resistance",
                "support_strength",
                "resistance_strength",
                "distance_to_support_pct",
                "distance_to_resistance_pct",
                "breakout_zone_lower",
                "breakout_zone_upper",
                "breakdown_zone_lower",
                "breakdown_zone_upper",
                "signal_level",
                "signal_value",
            ]
        ]
        
        X = X.apply(
            pd.to_numeric,
            errors="coerce",
        )

        X = X.fillna(0.0)
        
        sr_numeric_columns = [
            "support_strength",
            "resistance_strength",
            "distance_to_support_pct",
            "distance_to_resistance_pct",
            "breakout_zone_lower",
            "breakout_zone_upper",
            "breakdown_zone_lower",
            "breakdown_zone_upper",
            "signal_level",
        ]

        for column in sr_numeric_columns:

            dataset[column] = pd.to_numeric(
                dataset[column],
                errors="coerce",
            ).fillna(0.0)

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
            f"models/xgboost/{symbol.lower()}_xgb_{horizon}.pkl"
        )

        joblib.dump(
            list(X.columns),
            f"models/xgboost/{symbol.lower()}_xgb_features_{horizon}.pkl"
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
            "Symbol:",
            symbol
        )
        
        print(
            "Horizon:",
            horizon
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
            
        return {
            "symbol": symbol,
            "horizon": horizon,
            "mae": float(mae),
            "rmse": float(rmse),
            "mape": float(mape),
            "directional_accuracy": float(
                directional_accuracy
            ),
        }

    finally:
        db.close()


if __name__ == "__main__":
    train(
        horizon="5d"
    )