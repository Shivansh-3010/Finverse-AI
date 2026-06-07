from pydantic import BaseModel


class MarketDataResponse(BaseModel):
    symbol: str
    source: str
    status: str