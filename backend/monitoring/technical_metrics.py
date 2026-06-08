from dataclasses import dataclass


@dataclass
class TechnicalMetrics:
    indicator_calculations: int = 0
    indicator_errors: int = 0
    feature_generations: int = 0
    cache_hits: int = 0


technical_metrics = TechnicalMetrics()