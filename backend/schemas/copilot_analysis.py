from pydantic import BaseModel


class CopilotAnalysisResponse(BaseModel):
    symbol: str
    technical_score: int
    trend: str
    explanation: str