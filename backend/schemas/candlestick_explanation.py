from pydantic import BaseModel


class CandlestickExplanation(
    BaseModel
):
    pattern: str
    signal: str
    reason: str