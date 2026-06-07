from repositories.ohlcv_repository import OHLCVRepository


class MarketDataService:

    def __init__(self, repository: OHLCVRepository):
        self.repository = repository

    def save_market_data(self, df):

        records = df.to_dict(
            orient="records"
        )

        self.repository.bulk_insert(
            records
        )