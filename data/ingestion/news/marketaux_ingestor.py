import os
import requests

from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]

load_dotenv(
    PROJECT_ROOT / "backend" / ".env.development"
)


class MarketauxIngestor:

    BASE_URL = "https://api.marketaux.com/v1/news/all"

    def __init__(self):
        self.api_key = os.getenv("MARKETAUX_API_KEY")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def get_company_news(
        self,
        symbols: str,
        limit: int = 20
    ):

        if not self.api_key:
            raise ValueError(
                "MARKETAUX_API_KEY is not configured"
            )

        params = {
            "symbols": symbols,
            "limit": limit,
            "api_token": self.api_key
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()