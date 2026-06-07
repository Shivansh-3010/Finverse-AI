import requests

import os
from dotenv import load_dotenv

load_dotenv("backend/.env.development")


class AlphaVantageIngestor:

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def get_daily_data(
        self,
        symbol: str
    ):

        if not self.api_key:
            raise ValueError(
                "ALPHA_VANTAGE_API_KEY is not configured"
            )

        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()