from services.candlestick_analysis_service import (
    CandlestickAnalysisService,
)


result = CandlestickAnalysisService.analyze(
    open_price=100,
    high_price=102,
    low_price=90,
    close_price=101,
)

print(result)