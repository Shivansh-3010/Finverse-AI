import pandas as pd

from database.session import SessionLocal

from forecasting.dataset_builder import DatasetBuilder
from forecasting.horizons import HORIZON_DAYS
from forecasting.news_feature_builder import NewsFeatureBuilder

from repositories.ohlcv_repository import OHLCVRepository
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

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)


class TrainingPipeline:

    @staticmethod
    def build_dataset(
        symbol: str,
        horizon: str,
    ) -> pd.DataFrame:

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
                    timeframe="1d",
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

            df = ohlcv_to_dataframe(records)

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
                horizon_days=HORIZON_DAYS[horizon],
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
                    how="left",
                )

                dataset["avg_news_score"] = (
                    dataset["avg_news_score"]
                    .fillna(0)
                )

                dataset["avg_news_confidence"] = (
                    dataset["avg_news_confidence"]
                    .fillna(0)
                )

            return dataset

        finally:
            db.close()