from dataclasses import dataclass


@dataclass
class PivotPoint:
    index: int
    price: float
    pivot_type: str  # "high" or "low"


@dataclass
class SupportResistanceLevel:
    level: float
    strength: float = 0.0
    
@dataclass
class ClusteredLevel:
    level: float
    touches: int
    level_type: str  # "support" or "resistance"
    
@dataclass
class LevelStrength:
    level: float
    level_type: str
    touches: int
    strength: float
    
@dataclass
class SupportResistanceAnalysis:
    supports: list
    resistances: list

    nearest_support: float | None
    nearest_resistance: float | None

    signal: str | None = None
    signal_level: float | None = None