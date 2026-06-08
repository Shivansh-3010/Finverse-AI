from dataclasses import dataclass


@dataclass
class PatternResult:
    pattern: str
    signal: str
    confidence: float
    strength: int
    reason: str


@dataclass
class CandlestickAnalysis:
    score: float
    signal: str
    confidence: float