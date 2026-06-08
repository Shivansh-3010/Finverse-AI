from pydantic import BaseModel


class TechnicalAnalysisResponse(BaseModel):
    technical_score: int
    trend: str
    rsi: float
    reasons: list[str]