from pydantic import BaseModel


class TimeframeSupportResistance(
    BaseModel
):
    timeframe: str

    nearest_support: float | None = None
    nearest_resistance: float | None = None

    signal: str | None = None


class MultiTimeframeSupportResistanceResponse(
    BaseModel
):
    levels: list[
        TimeframeSupportResistance
    ]