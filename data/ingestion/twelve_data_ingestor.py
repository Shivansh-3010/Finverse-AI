import os
import requests

from dotenv import load_dotenv

load_dotenv("backend/.env.development")


class TwelveDataIngestor:

    BASE_URL = "https://api.twelvedata.com/time_series"

    def __init__(self):
        self.api_key = os.getenv(
            "TWELVE_DATA_API_KEY"
        )

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def get_daily_data(
        self,
        symbol: str
    ):

        if not self.api_key:
            raise ValueError(
                "TWELVE_DATA_API_KEY is not configured"
            )

        params = {
            "symbol": symbol,
            "interval": "1day",
            "apikey": self.api_key,
            "outputsize": 100
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()