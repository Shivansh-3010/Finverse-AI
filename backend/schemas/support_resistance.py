from typing import List, Optional

from pydantic import BaseModel

from datetime import datetime


class SupportResistanceResponse(BaseModel):
    supports: List[float]
    resistances: List[float]

    nearest_support: Optional[float] = None
    nearest_resistance: Optional[float] = None

    signal: Optional[str] = None
    signal_level: Optional[float] = None
    
class SupportResistanceSnapshot(BaseModel):
    symbol: str
    timeframe: str
    timestamp: datetime

    nearest_support: float | None = None
    nearest_resistance: float | None = None

    signal: str | None = None
    signal_level: float | None = None

    class Config:
        from_attributes = True


class SupportResistanceHistoryResponse(
    BaseModel
):
    history: list[
        SupportResistanceSnapshot
    ]