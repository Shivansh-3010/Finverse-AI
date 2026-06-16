import pandas as pd


class NewsFeatureBuilder:

    @staticmethod
    def build(
        news_articles
    ):

        if not news_articles:

            return pd.DataFrame()

        rows = []

        for article in news_articles:

            rows.append(
                {
                    "date":
                        article.published_at.date(),

                    "news_score":
                        article.news_score or 0,

                    "confidence":
                        article.confidence or 0,

                    "sentiment":
                        article.sentiment,
                }
            )

        df = pd.DataFrame(rows)

        grouped = (
            df.groupby("date")
            .agg(
                {
                    "news_score": "mean",
                    "confidence": "mean",
                }
            )
            .reset_index()
        )

        grouped.rename(
            columns={
                "news_score":
                    "avg_news_score",

                "confidence":
                    "avg_news_confidence",
            },
            inplace=True,
        )

        article_counts = (
            df.groupby("date")
            .size()
            .reset_index(
                name="article_count"
            )
        )

        positive_counts = (
            df[
                df["sentiment"]
                == "positive"
            ]
            .groupby("date")
            .size()
            .reset_index(
                name="positive_count"
            )
        )

        negative_counts = (
            df[
                df["sentiment"]
                == "negative"
            ]
            .groupby("date")
            .size()
            .reset_index(
                name="negative_count"
            )
        )

        neutral_counts = (
            df[
                df["sentiment"]
                == "neutral"
            ]
            .groupby("date")
            .size()
            .reset_index(
                name="neutral_count"
            )
        )

        grouped = grouped.merge(
            article_counts,
            on="date",
            how="left"
        )

        grouped = grouped.merge(
            positive_counts,
            on="date",
            how="left"
        )

        grouped = grouped.merge(
            negative_counts,
            on="date",
            how="left"
        )

        grouped = grouped.merge(
            neutral_counts,
            on="date",
            how="left"
        )

        grouped = grouped.fillna(0)

        grouped["recent_article_count"] = (
            grouped["article_count"]
        )

        return grouped