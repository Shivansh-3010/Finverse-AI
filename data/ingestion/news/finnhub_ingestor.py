import os
import requests

from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]

load_dotenv(
    PROJECT_ROOT / "backend" / ".env.development"
)


class FinnhubIngestor:

    BASE_URL = "https://finnhub.io/api/v1/company-news"

    def __init__(self):
        self.api_key = os.getenv("FINNHUB_API_KEY")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def get_company_news(
        self,
        symbol: str,
        from_date: str,
        to_date: str
    ):

        if not self.api_key:
            raise ValueError(
                "FINNHUB_API_KEY is not configured"
            )

        params = {
            "symbol": symbol,
            "from": from_date,
            "to": to_date,
            "token": self.api_key
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()