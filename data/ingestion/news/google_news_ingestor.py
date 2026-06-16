import feedparser
from urllib.parse import quote_plus


class GoogleNewsIngestor:

    BASE_URL = (
        "https://news.google.com/rss/search?q="
    )

    def is_configured(self) -> bool:
        return True

    def get_company_news(
        self,
        query: str,
        limit: int = 20
    ):

        rss_url = (
            self.BASE_URL +
            quote_plus(query)
        )

        feed = feedparser.parse(
            rss_url
        )

        articles = []

        for entry in feed.entries[:limit]:

            articles.append(
                {
                    "title": entry.get(
                        "title",
                        ""
                    ),

                    "url": entry.get(
                        "link",
                        ""
                    ),

                    "published_at": entry.get(
                        "published",
                        ""
                    ),

                    "source": "Google News",

                    "provider": "google_news",

                    "provider_article_id": entry.get(
                        "link",
                        ""
                    ),
                }
            )

        return articles