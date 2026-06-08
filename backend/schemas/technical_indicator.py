from datetime import datetime

from pydantic import BaseModel


class TechnicalIndicatorResponse(BaseModel):
    symbol: str
    timestamp: datetime

    rsi: float
    mfi: float

    sma_20: float
    ema_20: float

    macd: float
    macd_signal: float

    adx: float

    atr: float

    obv: float
    vwap: float

    bb_upper: float
    bb_middle: float
    bb_lower: float

    class Config:
        from_attributes = True


class TechnicalIndicatorHistoryResponse(BaseModel):
    indicators: list[TechnicalIndicatorResponse]