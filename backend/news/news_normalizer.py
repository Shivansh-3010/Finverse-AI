class NewsNormalizer:

    @staticmethod
    def normalize_article(

        title: str,

        source: str,

        published_at: str,

        symbol: str,

        content: str,

        url: str,

        provider: str,

        provider_article_id: str,

        events: list | None = None,

        sentiment: str | None = None,

        confidence: float | None = None,

        news_score: int | None = None,
    ):

        return {

            "title": title,

            "source": source,

            "published_at": published_at,

            "symbol": symbol,

            "content": content,

            "url": url,

            "provider": provider,

            "provider_article_id":
                provider_article_id,

            "events":
                events or [],

            "sentiment":
                sentiment,

            "confidence":
                confidence,

            "news_score":
                news_score,
        }