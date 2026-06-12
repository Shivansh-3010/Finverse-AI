from services.support_resistance_service import (
    SupportResistanceService,
)


result = SupportResistanceService.analyze(
    symbol="RELIANCE",
    timeframe="1d",
)

print(result)