from historical_news.loaders.indian_financial_loader import (
    IndianFinancialLoader,
)
from historical_news.loaders.toi_loader import (
    TOILoader,
)
from historical_news.loaders.economic_times_loader import (
    EconomicTimesLoader,
)


class HistoricalNewsBackfillPipeline:

    def __init__(self):

        self.indian_loader = IndianFinancialLoader()

        self.toi_loader = TOILoader()

        self.et_loader = EconomicTimesLoader()

    def load_all(self):

        indian_records = self.indian_loader.load(
            "../datasets/historical_news/IndianFinancialNews.csv"
        )

        toi_records = self.toi_loader.load(
            "../datasets/historical_news/india-news-headlines.csv"
        )

        et_records = self.et_loader.load_directory(
            "../datasets/historical_news"
        )

        all_records = (
            indian_records
            + toi_records
            + et_records
        )

        return all_records