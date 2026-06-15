from datetime import datetime

from pydantic import BaseModel


class MarketDataResponse(BaseModel):

    symbol: str
    timeframe: str

    open: float
    high: float
    low: float
    close: float

    volume: float

    timestamp: datetime