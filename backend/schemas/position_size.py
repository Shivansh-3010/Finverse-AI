from pydantic import BaseModel


class PositionSizeResponse(
    BaseModel
):
    quantity: int
    max_risk_amount: float
    risk_per_share: float