from cache.market_data_cache import MarketDataCache
from repositories.ohlcv_repository import OHLCVRepository


class MarketDataService:

    def __init__(
        self,
        repository: OHLCVRepository,
        cache: MarketDataCache
    ):
        self.repository = repository
        self.cache = cache

    def save_market_data(self, df):

        df = df.dropna(
            subset=[
                "open",
                "high",
                "low",
                "close",
            ]
        )

        records = df.to_dict(
            orient="records"
        )

        self.repository.bulk_insert(
            records
        )
        
    
        
    def get_cached_stock(self, symbol: str):

        cache_key = f"stock:{symbol}"

        return self.cache.get(
            cache_key
        )
        
    def cache_stock(
        self,
        symbol: str,
        data: dict
    ):

        cache_key = f"stock:{symbol}"

        self.cache.set(
            cache_key,
            data,
            ttl=60
        )