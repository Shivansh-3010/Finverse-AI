import pandas as pd
import hashlib

from models.news_article import (
    NewsArticle,
)

from repositories.news_article_repository import (
    NewsArticleRepository,
)

from news.news_pipeline import (
    NewsPipeline,
)


class HistoricalNewsImportService:

    @staticmethod
    def import_csv(
        db,
        csv_path: str,
        symbol: str = "MARKET",
        provider: str = "historical_dataset",
        limit: int | None = None,
    ):

        df = pd.read_csv(
            csv_path
        )

        if limit:

            df = df.head(
                limit
            )

        pipeline = (
            NewsPipeline()
        )

        repository = (
            NewsArticleRepository(db)
        )

        imported = 0

        for idx, row in df.iterrows():

            try:

                title = str(
                    row.get(
                        "Title",
                        ""
                    )
                )

                description = str(
                    row.get(
                        "Description",
                        ""
                    )
                )

                headline = (
                    f"{title} "
                    f"{description}"
                ).strip()

                result = (
                    pipeline.analyze(
                        headline
                    )
                )

                provider_article_id = (
                    hashlib.md5(
                        headline.encode("utf-8")
                    ).hexdigest()
                )

                if repository.exists_by_provider_article_id(
                    provider,
                    provider_article_id
                ):
                    continue

                article = NewsArticle(

                    symbol=symbol,

                    title=title,

                    source=provider,

                    provider=provider,

                    provider_article_id=
                        provider_article_id,

                    events=",".join(
                        result["events"]
                    ),

                    published_at=
                        pd.to_datetime(
                            row["Date"]
                        ),

                    sentiment=
                        result["sentiment"],

                    confidence=
                        float(
                            result["confidence"]
                        ),

                    news_score=
                        int(
                            result["news_score"]
                        ),

                    url="",

                    content=headline,
                )

                repository.save(
                    article
                )

                imported += 1

            except Exception as e:

                print(
                    f"Skipped row {idx}: {e}"
                )

        return {
            "imported": imported,
            "total_rows": len(df),
        }