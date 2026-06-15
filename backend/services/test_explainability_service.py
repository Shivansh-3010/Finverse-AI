from services.recommendation_service import (
    RecommendationService,
)

from services.explainability_service import (
    ExplainabilityService,
)

result = (
    RecommendationService.generate(
        symbol="RELIANCE",
        timeframe="1d"
    )
)

explanation = (
    ExplainabilityService
    .explain_recommendation(
        result
    )
)

print(explanation)