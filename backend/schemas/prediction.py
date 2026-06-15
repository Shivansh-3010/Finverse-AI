from pydantic import BaseModel


class PredictionResponse(
    BaseModel
):
    symbol: str
    timeframe: str
    forecast: str
    confidence: float
    horizon: str