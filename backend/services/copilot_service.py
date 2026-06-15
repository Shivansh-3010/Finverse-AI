from schemas.copilot_analysis import (
    CopilotAnalysisResponse,
)

from services.recommendation_service import (
    RecommendationService,
)

from services.explainability_service import (
    ExplainabilityService,
)
from metrics.monitoring_metrics import (
    MonitoringMetrics,
)


class CopilotService:

    @staticmethod
    def analyze(
        symbol: str
    ) -> CopilotAnalysisResponse:

        recommendation = (
            RecommendationService.generate(
                symbol=symbol
            )
        )

        if (
            recommendation.get(
                "recommendation"
            ) == "UNKNOWN"
        ):

            return CopilotAnalysisResponse(
                symbol=symbol,
                technical_score=0,
                trend="unknown",
                explanation=
                    recommendation.get(
                        "error",
                        "Analysis unavailable"
                    )
            )

        explanation = (
            ExplainabilityService
            .explain_recommendation(
                recommendation
            )
        )
        
        MonitoringMetrics.increment_copilot_requests()

        return CopilotAnalysisResponse(
            symbol=symbol,

            technical_score=
                recommendation[
                    "technical_score"
                ],

            trend=
                recommendation[
                    "trend"
                ],

            explanation=
                explanation
        )