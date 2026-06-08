from pydantic import BaseModel


class IndicatorExplanation(BaseModel):
    indicator: str
    value: float
    signal: str
    reason: str