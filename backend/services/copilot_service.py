from schemas.copilot_analysis import CopilotAnalysisResponse

from services.technical_analysis_service import (
    TechnicalAnalysisService,
)
from services.explainability_service import (
    ExplainabilityService,
)


class CopilotService:

    @staticmethod
    def analyze(symbol: str) -> CopilotAnalysisResponse:

        technical = TechnicalAnalysisService.analyze(symbol)

        explanation = ExplainabilityService.explain_rsi(
            technical["rsi"]
        )

        return CopilotAnalysisResponse(
            symbol=symbol,
            technical_score=technical["technical_score"],
            trend=technical["trend"],
            explanation=(
                f"{explanation.reason}. "
                f"Technical score is "
                f"{technical['technical_score']}."
            )
        )