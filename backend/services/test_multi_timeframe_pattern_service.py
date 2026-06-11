from services.multi_timeframe_pattern_service import (
    MultiTimeframePatternService,
)

result = (
    MultiTimeframePatternService.analyze(
        "RELIANCE"
    )
)

print(result)