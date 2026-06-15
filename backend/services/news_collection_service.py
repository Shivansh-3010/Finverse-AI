import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(
        str(PROJECT_ROOT)
    )

from data.ingestion.provider_manager import (
    ProviderManager
)

from news.news_normalizer import (
    NewsNormalizer
)

from news.news_pipeline import (
    NewsPipeline
)

from services.news_embedding_service import (
    NewsEmbeddingService
)

from metrics.monitoring_metrics import (
    MonitoringMetrics,
)

from datetime import (
    datetime,
    timedelta,
    timezone,
)


class NewsCollectionService:

    def __init__(self):

        self.providers = (
            ProviderManager()
        )

        self.normalizer = (
            NewsNormalizer()
        )
        
        self.pipeline = (
            NewsPipeline()
        )
        
        self.embedding_service = (
            NewsEmbeddingService()
        )

    def get_available_news_providers(self):

        available = []

        if self.providers.newsapi.is_configured():
            available.append("NewsAPI")

        if self.providers.finnhub.is_configured():
            available.append("Finnhub")

        if self.providers.marketaux.is_configured():
            available.append("Marketaux")

        return available
    
    def get_company_news(
        self,
        symbol: str
    ):

        articles = []

        if (
            self.providers.finnhub
            .is_configured()
        ):

            try:

                to_date = (
                    datetime.utcnow()
                    .date()
                )

                from_date = (
                    to_date -
                    timedelta(days=7)
                )

                finnhub_news = (
                    self.providers.finnhub
                    .get_company_news(
                        symbol=symbol,
                        from_date=
                            str(from_date),
                        to_date=
                            str(to_date)
                    )
                )

                for article in finnhub_news:

                    normalized_article = (
                        self.normalizer
                        .normalize_article(

                            title=
                                article.get(
                                    "headline",
                                    ""
                                ),

                            source=
                                article.get(
                                    "source",
                                    ""
                                ),

                            published_at=
                                datetime.fromtimestamp(
                                    article.get(
                                        "datetime",
                                        0
                                    ),
                                    tz=timezone.utc
                                ).isoformat(),

                            symbol=symbol,

                            content=
                                article.get(
                                    "summary",
                                    ""
                                ),

                            url=
                                article.get(
                                    "url",
                                    ""
                                ),

                            provider="finnhub",

                            provider_article_id=
                                str(
                                    article.get(
                                        "id",
                                        ""
                                    )
                                ),
                        )
                    )
                    
                    analysis = (
                        self.pipeline.analyze(
                            normalized_article[
                                "title"
                            ]
                        )
                    )

                    normalized_article[
                        "events"
                    ] = analysis[
                        "events"
                    ]

                    normalized_article[
                        "sentiment"
                    ] = analysis[
                        "sentiment"
                    ]

                    normalized_article[
                        "confidence"
                    ] = analysis[
                        "confidence"
                    ]

                    normalized_article[
                        "news_score"
                    ] = analysis[
                        "news_score"
                    ]
                    
                    self.embedding_service.store_article(
                        normalized_article
                    )

                    articles.append(
                        normalized_article
                    )
                    
                    MonitoringMetrics.increment_articles_processed()

            except Exception:

                pass

        return articles
    
    def get_company_news_newsapi(
        self,
        symbol: str
    ):

        articles = []

        if (
            self.providers.newsapi
            .is_configured()
        ):

            try:

                response = (
                    self.providers.newsapi
                    .get_company_news(
                        query=symbol
                    )
                )

                for article in (
                    response.get(
                        "articles",
                        []
                    )
                ):

                    normalized_article = (
                        self.normalizer
                        .normalize_article(

                            title=
                                article.get(
                                    "title",
                                    ""
                                ),

                            source=
                                article.get(
                                    "source",
                                    {}
                                ).get(
                                    "name",
                                    ""
                                ),

                            published_at=
                                article.get(
                                    "publishedAt",
                                    ""
                                ),

                            symbol=symbol,

                            content=
                                article.get(
                                    "description",
                                    ""
                                ) or "",

                            url=
                                article.get(
                                    "url",
                                    ""
                                ),

                            provider="newsapi",

                            provider_article_id=
                                article.get(
                                    "url",
                                    ""
                                ),
                        )
                    )

                    analysis = (
                        self.pipeline.analyze(
                            normalized_article[
                                "title"
                            ]
                        )
                    )

                    normalized_article[
                        "events"
                    ] = analysis[
                        "events"
                    ]

                    normalized_article[
                        "sentiment"
                    ] = analysis[
                        "sentiment"
                    ]

                    normalized_article[
                        "confidence"
                    ] = analysis[
                        "confidence"
                    ]

                    normalized_article[
                        "news_score"
                    ] = analysis[
                        "news_score"
                    ]
                    
                    self.embedding_service.store_article(
                        normalized_article
                    )

                    articles.append(
                        normalized_article
                    )
                    
                    MonitoringMetrics.increment_articles_processed()

            except Exception as e:

                print(
                    f"NewsAPI Error: {e}"
                )

        return articles
    
    def get_company_news_combined(
        self,
        symbol: str
    ):

        articles = []

        finnhub_articles = (
            self.get_company_news(
                symbol
            )
        )

        newsapi_articles = (
            self.get_company_news_newsapi(
                symbol
            )
        )

        articles.extend(
            finnhub_articles
        )

        articles.extend(
            newsapi_articles
        )

        if (
            len(finnhub_articles) == 0
            and
            len(newsapi_articles) == 0
        ):

            articles.extend(
                self.get_company_news_marketaux(
                    symbol
                )
            )

        seen_titles = set()

        unique_articles = []

        for article in articles:

            title = (
                article["title"]
                .strip()
                .lower()
            )

            if title in seen_titles:
                continue

            seen_titles.add(
                title
            )

            unique_articles.append(
                article
            )

        unique_articles.sort(
            key=lambda article:
                article.get(
                    "published_at",
                    ""
                ),
            reverse=True
        )

        return unique_articles[:100]
    
    def get_company_news_marketaux(
        self,
        symbol: str
    ):

        articles = []

        if (
            self.providers.marketaux
            .is_configured()
        ):

            try:

                response = (
                    self.providers.marketaux
                    .get_company_news(
                        symbols=symbol,
                        limit=20
                    )
                )

                for article in (
                    response.get(
                        "data",
                        []
                    )
                ):

                    normalized_article = (
                        self.normalizer
                        .normalize_article(

                            title=
                                article.get(
                                    "title",
                                    ""
                                ),

                            source=
                                article.get(
                                    "source",
                                    ""
                                ),

                            published_at=
                                article.get(
                                    "published_at",
                                    ""
                                ),

                            symbol=symbol,

                            content=
                                article.get(
                                    "description",
                                    ""
                                ) or "",

                            url=
                                article.get(
                                    "url",
                                    ""
                                ),

                            provider="marketaux",

                            provider_article_id=
                                str(
                                    article.get(
                                        "uuid",
                                        ""
                                    )
                                ),
                        )
                    )

                    articles.append(
                        normalized_article
                    )
                    
                    MonitoringMetrics.increment_articles_processed()

            except Exception:

                pass

        return articles