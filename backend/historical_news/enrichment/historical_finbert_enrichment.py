import pandas as pd
from tqdm import tqdm

from services.finbert_service import (
    FinBERTService,
)


class HistoricalFinBERTEnrichment:

    def __init__(self):

        self.finbert = (
            FinBERTService()
        )

    def enrich(
        self,
        input_csv: str,
        output_csv: str,
        limit: int | None = None,
    ):

        df = pd.read_csv(
            input_csv,
            low_memory=False,
        )

        if limit:
            df = df.head(limit)

        sentiments = []
        confidences = []

        checkpoint_interval = 1000

        checkpoint_file = (
            output_csv.replace(
                ".csv",
                "_checkpoint.csv"
            )
        )

        for _, row in tqdm(
            df.iterrows(),
            total=len(df),
            desc="FinBERT Enrichment",
        ):

            title = str(
                row.get(
                    "title",
                    ""
                )
            )

            description = str(
                row.get(
                    "description",
                    ""
                )
            )

            text = (
                f"{title} {description}"
            ).strip()

            try:

                result = (
                    self.finbert.analyze(
                        text
                    )
                )

                sentiments.append(
                    result["sentiment"]
                )

                confidences.append(
                    result["confidence"]
                )

            except Exception as e:

                print(
                    f"Error processing row: {e}"
                )

                sentiments.append(
                    "neutral"
                )

                confidences.append(
                    0.0
                )

            if (
                len(sentiments)
                % checkpoint_interval
                == 0
            ):

                temp_df = (
                    df.iloc[
                        :len(sentiments)
                    ].copy()
                )

                temp_df[
                    "sentiment"
                ] = sentiments

                temp_df[
                    "confidence"
                ] = confidences

                temp_df.to_csv(
                    checkpoint_file,
                    index=False,
                )

                print(
                    f"Checkpoint saved: "
                    f"{len(sentiments)} rows"
                )

        df["sentiment"] = sentiments
        df["confidence"] = confidences

        df.to_csv(
            output_csv,
            index=False,
        )

        print(
            f"Final output saved: "
            f"{output_csv}"
        )

        return {
            "rows": len(df),
            "output": output_csv,
            "checkpoint": checkpoint_file,
        }