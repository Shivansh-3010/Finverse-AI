import pandas as pd

from historical_news.models.historical_news_record import (
    HistoricalNewsRecord,
)


class TOILoader:

    BUSINESS_CATEGORIES = [
        "business.india-business",
        "business.international-business",
    ]

    def load(self, file_path: str) -> list[HistoricalNewsRecord]:

        df = pd.read_csv(
            file_path,
            usecols=[
                "publish_date",
                "headline_category",
                "headline_text",
            ]
        )

        df = df[
            df["headline_category"].isin(
                self.BUSINESS_CATEGORIES
            )
        ]

        records = []

        for _, row in df.iterrows():

            record = HistoricalNewsRecord(
                date=pd.to_datetime(
                    str(row["publish_date"]),
                    format="%Y%m%d"
                ),
                title=str(row["headline_text"]).strip(),
                description=None,
                source="toi_business",
            )

            records.append(record)

        return records