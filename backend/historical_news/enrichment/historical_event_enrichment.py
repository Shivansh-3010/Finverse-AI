import pandas as pd
from tqdm import tqdm

from news.event_detection.event_detector import (
    EventDetector,
)


class HistoricalEventEnrichment:

    def __init__(self):

        self.detector = (
            EventDetector()
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

        events = []

        for _, row in tqdm(
            df.iterrows(),
            total=len(df),
            desc="Event Detection",
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

            detected = (
                self.detector.detect_events(
                    text
                )
            )

            events.append(
                ",".join(detected)
            )

        df["events"] = events

        df.to_csv(
            output_csv,
            index=False,
        )

        return {
            "rows": len(df),
            "output": output_csv,
        }