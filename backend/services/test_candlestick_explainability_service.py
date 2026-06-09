from services.candlestick_explainability_service import (
    CandlestickExplainabilityService,
)


result = (
    CandlestickExplainabilityService.explain(
        "Hammer"
    )
)

print(result)