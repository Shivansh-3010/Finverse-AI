import pandas as pd
import numpy as np


class NewsFeatureStoreV2Generator:

    def generate(
        self,
        input_csv: str,
        output_csv: str,
    ):

        df = pd.read_csv(
            input_csv,
            low_memory=False,
        )

        df["date"] = pd.to_datetime(
            df["date"]
        )

        df = df.sort_values(
            ["symbol", "date"]
        )

        #
        # Statistical Features
        #

        df["sentiment_momentum"] = (
            df["positive_ratio"]
            - df["negative_ratio"]
        )

        df["event_intensity"] = np.where(
            df["news_count"] > 0,
            df["event_score"]
            / df["news_count"],
            0.0,
        )

        #
        # Confidence Features
        #

        df["positive_confidence"] = (
            df["positive_confidence_mean"]
        )

        df["negative_confidence"] = (
            df["negative_confidence_mean"]
        )

        df["neutral_confidence"] = (
            df["neutral_confidence_mean"]
        )


        #
        # Event Article Ratio
        #

        event_article_count = (
            df["earnings_count"]
            + df["funding_count"]
            + df["regulatory_count"]
            + df["macro_count"]
            + df[
                "mergers_acquisitions_count"
            ]
        )

        df["event_article_ratio"] = np.where(
            df["news_count"] > 0,
            event_article_count
            / df["news_count"],
            0.0,
        )

        #
        # Dominant Sentiment
        #

        df["dominant_sentiment"] = 0

        df.loc[
            df["positive_count"]
            > df["negative_count"],
            "dominant_sentiment",
        ] = 1

        df.loc[
            df["negative_count"]
            > df["positive_count"],
            "dominant_sentiment",
        ] = -1

        #
        # Binary Event Flags
        #

        df["has_earnings_event"] = (
            df["earnings_count"] > 0
        ).astype(int)

        df["has_regulatory_event"] = (
            df["regulatory_count"] > 0
        ).astype(int)

        df["has_funding_event"] = (
            df["funding_count"] > 0
        ).astype(int)

        df["has_ma_event"] = (
            df[
                "mergers_acquisitions_count"
            ] > 0
        ).astype(int)

        #
        # Rolling Features
        #

        grouped = df.groupby(
            "symbol",
            group_keys=False,
        )

        return self._build_rolling_features(
            df,
            grouped,
            output_csv,
        )
        
    def _build_rolling_features(
        self,
        df,
        grouped,
        output_csv,
    ):

        result_frames = []

        for symbol, group in grouped:

            group = (
                group
                .sort_values("date")
                .copy()
            )

            group = (
                group
                .set_index("date")
            )

            #
            # 3 Day Windows
            #

            group["news_count_3d"] = (
                group["news_count"]
                .rolling("3D")
                .sum()
            )

            group["sentiment_score_3d"] = (
                group["sentiment_score"]
                .rolling("3D")
                .mean()
            )

            group["event_score_3d"] = (
                group["event_score"]
                .rolling("3D")
                .mean()
            )

            #
            # 7 Day Windows
            #

            group["news_count_7d"] = (
                group["news_count"]
                .rolling("7D")
                .sum()
            )

            group["sentiment_score_7d"] = (
                group["sentiment_score"]
                .rolling("7D")
                .mean()
            )

            group["event_score_7d"] = (
                group["event_score"]
                .rolling("7D")
                .mean()
            )

            group = (
                group
                .reset_index()
            )

            result_frames.append(
                group
            )

        df = pd.concat(
            result_frames,
            ignore_index=True,
        )

        df["rolling_news_momentum"] = (
            df["sentiment_score_7d"]
            * df["event_score_7d"]
        )
        
        df["news_attention_score"] = (
            df["news_count_7d"]
            * abs(
                df["sentiment_score_7d"]
            )
        )

        df.to_csv(
            output_csv,
            index=False,
        )

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "output": output_csv,
        }