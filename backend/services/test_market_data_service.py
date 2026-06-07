from backend.cache.market_data_cache import MarketDataCache
from backend.services.market_data_service import MarketDataService


cache = MarketDataCache()

service = MarketDataService(
    repository=None,
    cache=cache
)

service.cache_stock(
    "RELIANCE",
    {
        "price": 1291,
        "volume": 17785223
    }
)

result = service.get_cached_stock(
    "RELIANCE"
)

print(result)