import hashlib
from pathlib import Path

import pandas as pd

from models.news_article import (
    NewsArticle,
)

from repositories.news_article_repository import (
    NewsArticleRepository,
)

from news.news_pipeline import (
    NewsPipeline,
)
from config.company_news_mapping import (
    COMPANY_SYMBOL_MAPPING,
)


class CompanyNewsImportService:

    @staticmethod
    def import_csv(
        db,
        csv_path: str,
        provider: str = "company_dataset",
        limit: int | None = None,
    ):

        csv_file = Path(
            csv_path
        )
        
        symbol = COMPANY_SYMBOL_MAPPING.get(
            csv_file.name
        )

        if not symbol:
            raise ValueError(
                f"No mapping found for {csv_file.name}"
            )

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

        pipeline = (
            NewsPipeline()
        )

        imported = 0

        for idx, row in df.iterrows():

            try:

                title = str(
                    row.get(
                        "Title",
                        ""
                    )
                ).strip()

                description = str(
                    row.get(
                        "Article Description",
                        ""
                    )
                ).strip()

                url = str(
                    row.get(
                        "URL",
                        ""
                    )
                ).strip()

                content = (
                    f"{title} "
                    f"{description}"
                ).strip()

                provider_article_id = (
                    hashlib.md5(
                        url.encode(
                            "utf-8"
                        )
                    ).hexdigest()
                )

                if (
                    repository
                    .exists_by_provider_article_id(
                        provider,
                        provider_article_id,
                    )
                ):
                    continue

                result = (
                    pipeline.analyze(
                        content
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
                        result["events"]
                    ),

                    published_at=
                        pd.to_datetime(
                            row["Date"],
                            dayfirst=True,
                        ),

                    sentiment=
                        result[
                            "sentiment"
                        ],

                    confidence=
                        float(
                            result[
                                "confidence"
                            ]
                        ),

                    news_score=
                        int(
                            result[
                                "news_score"
                            ]
                        ),

                    url=url,

                    content=content,
                )

                repository.save(
                    article
                )

                imported += 1

                if (
                    imported % 100 == 0
                ):
                    print(
                        f"Imported "
                        f"{imported} rows..."
                    )

            except Exception as e:

                print(
                    f"Skipped row "
                    f"{idx}: {e}"
                )

        print(
            f"\nImport Complete:"
            f" {imported} rows"
        )

        return {

            "symbol":
                symbol,

            "imported":
                imported,

            "total_rows":
                len(df),
        }