from historical_news.models.historical_news_record import (
    HistoricalNewsRecord,
)


class NewsDeduplicator:

    @staticmethod
    def deduplicate(
        records: list[HistoricalNewsRecord],
    ) -> list[HistoricalNewsRecord]:

        unique_records = {}
        
        for record in records:

            if record.news_hash not in unique_records:
                unique_records[record.news_hash] = record

        return list(unique_records.values())