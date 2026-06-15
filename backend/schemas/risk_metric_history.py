from pydantic import BaseModel


class RiskMetricHistoryItem(
    BaseModel
):
    symbol: str
    timeframe: str
    volatility: float
    drawdown: float
    var_95: float
    expected_shortfall: float
    risk_score: int
    risk_category: str


class RiskMetricHistoryResponse(
    BaseModel
):
    metrics: list[RiskMetricHistoryItem]