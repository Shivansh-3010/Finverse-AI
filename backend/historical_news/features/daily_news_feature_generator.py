import pandas as pd
from tqdm import tqdm

from historical_news.features.sentiment_features import (
    SentimentFeatureBuilder,
)

from historical_news.features.event_features import (
    EventFeatureBuilder,
)


class DailyNewsFeatureGenerator:

    def generate(
        self,
        input_csv: str,
        output_csv: str,
    ):

        df = pd.read_csv(
            input_csv,
            low_memory=False,
        )

        df = df[
            df["symbols"].notna()
            & (df["symbols"] != "")
        ].copy()
        
        df["symbols"] = (
            df["symbols"]
            .str.split(",")
        )

        df = df.explode(
            "symbols"
        )

        df["symbols"] = (
            df["symbols"]
            .str.strip()
        )

        df["date"] = pd.to_datetime(
            df["date"]
        ).dt.date

        records = []

        grouped = df.groupby(
            ["date", "symbols"]
        )

        for (
            (date, symbol),
            group
        ) in tqdm(
            grouped,
            total=len(grouped),
            desc="Generating Daily News Features",
        ):

            sentiment_features = (
                SentimentFeatureBuilder.build(
                    group
                )
            )

            event_features = (
                EventFeatureBuilder.build(
                    group
                )
            )

            row = {

                "date": date,

                "symbol": symbol,
            }

            row.update(
                sentiment_features
            )

            row.update(
                event_features
            )

            records.append(
                row
            )

        features_df = pd.DataFrame(
            records
        )

        features_df.to_csv(
            output_csv,
            index=False,
        )

        return {
            "rows": len(features_df),
            "output": output_csv,
        }