import math
from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository,
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


class FeatureBuilder:

    @staticmethod
    def build(
        db,
        symbol: str,
        timeframe: str = "1d"
    ):

        technical = (
            TechnicalIndicatorRepository(db)
            .get_latest_by_timeframe(
                symbol,
                timeframe
            )
        )

        pattern = (
            CandlestickPatternRepository(db)
            .get_latest_by_timeframe(
                symbol,
                timeframe
            )
        )

        news = (
            NewsArticleRepository(db)
            .get_combined_summary(
                symbol
            )
        )

        risk = (
            RiskMetricRepository(db)
            .get_latest(
                symbol,
                timeframe
            )
        )
        
        support_resistance = (
            SupportResistanceRepository(db)
            .get_latest_by_timeframe(
                symbol,
                timeframe
            )
        )
        
        signal_map = {
            "support": 1.0,
            "resistance": -1.0,
            "breakout": 2.0,
            "breakdown": -2.0,
        }

        signal_value = signal_map.get(
            getattr(
                support_resistance,
                "signal",
                None,
            ),
            0.0,
        )

        features = [
            getattr(technical, "rsi", 0.0),
            getattr(technical, "macd", 0.0),
            getattr(technical, "macd_signal", 0.0),
            getattr(technical, "atr", 0.0),
            getattr(technical, "adx", 0.0),
            getattr(technical, "mfi", 0.0),
            getattr(technical, "obv", 0.0),
            getattr(technical, "vwap", 0.0),
            getattr(technical, "bb_upper", 0.0),
            getattr(technical, "bb_middle", 0.0),
            getattr(technical, "bb_lower", 0.0),

            getattr(pattern, "strength", 0.0),
            getattr(pattern, "confidence", 0.0),
            getattr(pattern, "candlestick_score", 0.0),

            news["avg_news_score"],
            news["avg_confidence"],
            news["article_count"],
            news["recent_article_count"],
            news["positive_count"],
            news["negative_count"],
            news["neutral_count"],
            
            # Risk Features

            getattr(
                risk,
                "volatility_252d",
                0.0,
            ),

            getattr(
                risk,
                "drawdown_252d",
                0.0,
            ),

            getattr(
                risk,
                "var95_252d",
                0.0,
            ),

            getattr(
                risk,
                "expected_shortfall_252d",
                0.0,
            ),

            getattr(
                risk,
                "risk_score",
                0.0,
            ),
            
            # Support & Resistance Features

            getattr(
                support_resistance,
                "nearest_support",
                0.0,
            ),

            getattr(
                support_resistance,
                "nearest_resistance",
                0.0,
            ),

            getattr(
                support_resistance,
                "support_strength",
                0.0,
            ),

            getattr(
                support_resistance,
                "resistance_strength",
                0.0,
            ),

            getattr(
                support_resistance,
                "distance_to_support_pct",
                0.0,
            ),

            getattr(
                support_resistance,
                "distance_to_resistance_pct",
                0.0,
            ),

            getattr(
                support_resistance,
                "breakout_zone_lower",
                0.0,
            ),

            getattr(
                support_resistance,
                "breakout_zone_upper",
                0.0,
            ),

            getattr(
                support_resistance,
                "breakdown_zone_lower",
                0.0,
            ),

            getattr(
                support_resistance,
                "breakdown_zone_upper",
                0.0,
            ),

            getattr(
                support_resistance,
                "signal_level",
                0.0,
            ),

            signal_value,
        ]

        return [
            0.0
            if (
                value is None
                or (
                    isinstance(value, float)
                    and math.isnan(value)
                )
            )
            else float(value)
            for value in features
        ]