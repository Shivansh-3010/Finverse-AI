import json

from redis import Redis

from backend.core.settings import settings


class MarketDataCache:

    def __init__(self):
        self.redis = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )

    def get(self, key: str):

        data = self.redis.get(key)

        if data:
            return json.loads(data)

        return None

    def set(
        self,
        key: str,
        value,
        ttl: int = 60
    ):

        self.redis.set(
            key,
            json.dumps(value),
            ex=ttl
        )