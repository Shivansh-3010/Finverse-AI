from datetime import datetime

from pydantic import BaseModel


class CandlestickPatternItem(BaseModel):
    symbol: str
    timestamp: datetime

    pattern_name: str
    signal: str

    strength: float
    candlestick_score: float


class CandlestickPatternHistoryResponse(
    BaseModel
):
    patterns: list[
        CandlestickPatternItem
    ]