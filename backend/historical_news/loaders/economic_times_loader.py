from pathlib import Path

import pandas as pd

from historical_news.models.historical_news_record import (
    HistoricalNewsRecord,
)


class EconomicTimesLoader:

    FILE_PATTERN = "economic_times_headlines_*.csv"

    def load_directory(
        self,
        directory_path: str,
    ) -> list[HistoricalNewsRecord]:

        directory = Path(directory_path)

        records = []

        for file in sorted(
            directory.glob(self.FILE_PATTERN)
        ):

            print(f"Loading {file.name}")

            df = pd.read_csv(
                file,
                usecols=[
                    "Date",
                    "Headline",
                    "Headline link",
                ]
            )

            for _, row in df.iterrows():

                record = HistoricalNewsRecord(
                    date=pd.to_datetime(
                        row["Date"],
                        format="%d-%m-%Y"
                    ),
                    title=str(row["Headline"]).strip(),
                    description=None,
                    source="economic_times",
                )

                records.append(record)

        return records