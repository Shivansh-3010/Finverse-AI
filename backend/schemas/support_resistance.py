from typing import List, Optional

from pydantic import BaseModel


class SupportResistanceResponse(BaseModel):
    supports: List[float]
    resistances: List[float]

    nearest_support: Optional[float] = None
    nearest_resistance: Optional[float] = None

    signal: Optional[str] = None
    signal_level: Optional[float] = None