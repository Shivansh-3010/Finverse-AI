from services.recommendation_service import (
    RecommendationService,
)

result = (
    RecommendationService.generate(
        symbol="AAPL",
        timeframe="1d"
    )
)

print(result)