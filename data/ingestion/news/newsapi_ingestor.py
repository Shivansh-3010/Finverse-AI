import os
import requests

from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]

load_dotenv(
    PROJECT_ROOT / "backend" / ".env.development"
)


class NewsAPIIngestor:

    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        self.api_key = os.getenv("NEWSAPI_API_KEY")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def get_company_news(
        self,
        query: str,
        page_size: int = 100,
        from_date: str | None = None,
        to_date: str | None = None,
    ):

        if not self.api_key:
            raise ValueError(
                "NEWSAPI_API_KEY is not configured"
            )

        params = {
            "q": query,
            "searchIn": "title",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "apiKey": self.api_key
        }
        
        if from_date:
            params["from"] = from_date

        if to_date:
            params["to"] = to_date

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()