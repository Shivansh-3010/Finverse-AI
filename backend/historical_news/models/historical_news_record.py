from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class HistoricalNewsRecord(BaseModel):
    """
    Unified schema used by all historical news datasets.
    """

    date: datetime

    title: str

    description: Optional[str] = None

    source: str

    symbols: List[str] = []

    sentiment_label: Optional[str] = None

    sentiment_score: Optional[float] = None

    event_type: Optional[str] = None

    news_hash: Optional[str] = None