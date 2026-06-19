import hashlib
import pandas as pd

from models.news_article import (
    NewsArticle,
)

from repositories.news_article_repository import (
    NewsArticleRepository,
)

from news.event_detection.event_detector import (
    EventDetector,
)

from news.event_detection.event_scoring import (
    EventScoring,
)

from news.news_score_engine import (
    NewsScoreEngine,
)


class SentimentNewsImportService:

    @staticmethod
    def import_csv(
        db,
        csv_path: str,
        symbol: str = "MARKET",
        provider: str = "sentiment_dataset",
        limit: int | None = None,
    ):

        df = pd.read_csv(
            csv_path
        )

        if limit:

            df = df.head(
                limit
            )

        repository = (
            NewsArticleRepository(db)
        )

        detector = (
            EventDetector()
        )

        imported = 0

        for idx, row in df.iterrows():

            try:

                title = str(
                    row["Title"]
                ).strip()

                url = str(
                    row["URL"]
                ).strip()

                sentiment = (
                    str(
                        row["sentiment"]
                    )
                    .lower()
                    .strip()
                )

                confidence = abs(
                    float(
                        row["confidence"]
                    )
                )

                provider_article_id = (
                    hashlib.md5(
                        url.encode("utf-8")
                    ).hexdigest()
                )

                if repository.exists_by_provider_article_id(
                    provider,
                    provider_article_id,
                ):
                    continue

                events = (
                    detector.detect_events(
                        title
                    )
                )

                event_score = (
                    EventScoring.get_score(
                        events
                    )
                )

                news_score = (
                    NewsScoreEngine.calculate_score(
                        sentiment=sentiment,
                        confidence=confidence,
                        event_score=event_score,
                    )
                )

                article = NewsArticle(

                    symbol=symbol,

                    title=title,

                    source=provider,

                    provider=provider,

                    provider_article_id=
                        provider_article_id,

                    events=",".join(
                        events
                    ),

                    published_at=
                        pd.to_datetime(
                            row["Date"],
                            format="%d/%m/%y"
                        ),

                    sentiment=
                        sentiment,

                    confidence=
                        confidence,

                    news_score=
                        int(
                            news_score
                        ),

                    url=url,

                    content=title,
                )

                repository.save(
                    article
                )

                imported += 1

                if (
                    imported % 5000 == 0
                    and imported > 0
                ):
                    print(
                        f"Imported {imported:,} rows..."
                    )

            except Exception as e:

                print(
                    f"Skipped row {idx}: {e}"
                )

        print(
            f"\nImport Complete: "
            f"{imported:,} rows imported"
        )

        return {

            "imported":
                imported,

            "total_rows":
                len(df),

            "provider":
                provider,
        }