from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)

from repositories.news_article_repository import (
    NewsArticleRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

from forecasting.dataset_builder import (
    DatasetBuilder,
)

from forecasting.news_feature_builder import (
    NewsFeatureBuilder,
)


def test_feature_coverage():

    db = SessionLocal()

    try:

        symbol = "RELIANCE"

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
                timeframe="1d"
            )
        )

        news_articles = (
            NewsArticleRepository(db)
            .get_history(
                symbol=symbol
            )
        )

        df = ohlcv_to_dataframe(records)

        candlestick_features = [
            {
                "timestamp": p.timestamp,
                "strength": p.strength,
                "confidence": p.confidence,
                "candlestick_score": p.candlestick_score,
            }
            for p in patterns
        ]

        import pandas as pd

        candlestick_features = pd.DataFrame(
            candlestick_features
        )

        news_features = (
            NewsFeatureBuilder.build(
                news_articles
            )
        )

        dataset = DatasetBuilder.build(
            df,
            candlestick_features,
            horizon_days=1,
        )

        total_rows = len(dataset)

        candlestick_rows = (
            dataset["strength"]
            .notna()
            .sum()
        )

        print("\n=== Candlestick Coverage ===")
        print("Total Rows:", total_rows)
        print("Rows With Candlestick Data:", candlestick_rows)
        print(
            "Coverage:",
            round(
                candlestick_rows / total_rows * 100,
                2
            ),
            "%"
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

            news_rows = (
                dataset["avg_news_score"]
                .notna()
                .sum()
            )

            print("\n=== News Coverage ===")
            print("Rows With News Data:", news_rows)
            print(
                "Coverage:",
                round(
                    news_rows / total_rows * 100,
                    2
                ),
                "%"
            )

        assert True

    finally:
        db.close()