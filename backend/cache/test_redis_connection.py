from cache.market_data_cache import MarketDataCache


cache = MarketDataCache()

cache.set(
    "healthcheck",
    {"status": "ok"},
    ttl=60
)

result = cache.get("healthcheck")

print(result)