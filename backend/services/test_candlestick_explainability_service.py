from services.candlestick_explainability_service import (
    CandlestickExplainabilityService,
)


result = (
    CandlestickExplainabilityService.explain(
        "Spinning Top"
    )
)

print(result)