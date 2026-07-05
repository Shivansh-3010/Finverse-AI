import hashlib

from historical_news.models.historical_news_record import (
    HistoricalNewsRecord,
)


class NewsNormalizer:

    @staticmethod
    def generate_hash(
        record: HistoricalNewsRecord,
    ) -> str:

        text = (
            f"{record.date.date()}|"
            f"{record.title.lower().strip()}"
        )

        return hashlib.md5(
            text.encode("utf-8")
        ).hexdigest()

    @classmethod
    def normalize(
        cls,
        record: HistoricalNewsRecord,
    ) -> HistoricalNewsRecord:

        record.news_hash = cls.generate_hash(
            record
        )

        return record