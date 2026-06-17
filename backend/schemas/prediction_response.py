from pydantic import BaseModel


class PredictionResponse(
    BaseModel
):

    symbol: str

    timeframe: str

    forecast: str

    confidence: float

    predicted_return_pct: float

    reason: str