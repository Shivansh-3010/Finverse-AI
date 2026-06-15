from pydantic import BaseModel


class RiskAnalysisResponse(
    BaseModel
):
    volatility: float
    drawdown: float
    var_95: float
    expected_shortfall: float
    risk_score: int
    risk_category: str
    reason: str