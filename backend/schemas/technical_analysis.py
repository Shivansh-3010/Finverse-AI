from pydantic import BaseModel


class TechnicalAnalysisResponse(BaseModel):
    technical_score: int
    candlestick_score: int
    combined_score: int

    trend: str
    rsi: float

    reasons: list[str]
    candlestick_patterns: list