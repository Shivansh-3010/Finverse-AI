from services.candlestick_analysis_service import (
    CandlestickAnalysisService,
)


result = CandlestickAnalysisService.analyze(
    "RELIANCE"
)

print(result)