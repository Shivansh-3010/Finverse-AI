from pathlib import Path

import pandas as pd

from historical_news.models.historical_news_record import (
    HistoricalNewsRecord,
)


class IndianFinancialLoader:

    def load(self, file_path: str) -> list[HistoricalNewsRecord]:

        df = pd.read_csv(file_path)

        records = []

        for _, row in df.iterrows():

            record = HistoricalNewsRecord(
                date=pd.to_datetime(row["Date"]),
                title=str(row["Title"]).strip(),
                description=str(row["Description"]).strip(),
                source="indian_financial_news",
            )

            records.append(record)

        return records