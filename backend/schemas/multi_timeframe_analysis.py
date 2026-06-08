from pydantic import BaseModel


class TimeframeSignal(BaseModel):
    timeframe: str
    trend: str


class MultiTimeframeAnalysisResponse(BaseModel):
    overall_trend: str
    signals: list[TimeframeSignal]