from pydantic import BaseModel


class CandlestickAnalysisResponse(BaseModel):
    candlestick_score: float
    patterns: list