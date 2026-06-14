from cache.market_data_cache import MarketDataCache


cache = MarketDataCache()

cache.set(
    "stock:RELIANCE",
    {"price": 1291},
    ttl=60
)

data = cache.get(
    "stock:RELIANCE"
)

print(data)