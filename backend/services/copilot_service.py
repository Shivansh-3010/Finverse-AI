from uuid import UUID
from sqlalchemy.orm import Session

from services.portfolio_intelligence_service import (
    portfolio_intelligence_service,
)
from services.portfolio_recommendation_service import (
    portfolio_recommendation_service,
)
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

    @staticmethod
    def analyze_portfolio(
        db: Session,
        portfolio_id: UUID,
        benchmark: str = "NIFTY50",
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:
        intelligence = portfolio_intelligence_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            benchmark=benchmark,
            timeframe=timeframe,
            lookback_days=lookback_days,
        )

        recommendation_result = (
            portfolio_recommendation_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                benchmark=benchmark,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        summary = intelligence.get("portfolio_summary") or {}
        recommendations = recommendation_result.get(
            "recommendations", []
        )

        risk_flags = intelligence.get("risk_flags") or []

        if intelligence.get("overall_risk_score") is None:
            summary_text = (
                "Portfolio analysis has insufficient risk-score data. "
                "Review the available metrics before making decisions."
            )
        else:
            summary_text = (
                f"Portfolio risk category: "
                f"{intelligence.get('intelligence_category', 'Unknown')}. "
                f"Positions: {summary.get('position_count', 'Unknown')}. "
                f"Risk flags: {len(risk_flags)}. "
                f"Prioritized recommendations: {len(recommendations)}."
            )

        MonitoringMetrics.increment_copilot_requests()

        return {
            "portfolio_id": str(portfolio_id),
            "benchmark": benchmark,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "summary": summary_text,
            "intelligence_category": intelligence.get(
                "intelligence_category"
            ),
            "overall_risk_score": intelligence.get(
                "overall_risk_score"
            ),
            "risk_flags": risk_flags,
            "portfolio_summary": summary,
            "recommendations": recommendations,
            "recommendation_count": len(recommendations),
            "message": (
                "Informational portfolio analysis, not a guarantee "
                "of future performance."
            ),
        }
