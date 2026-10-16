
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_intelligence_service import (
    portfolio_intelligence_service,
)


class PortfolioIntelligenceAgent:
    """
    Phase 12 Portfolio Intelligence Agent.

    Delegates portfolio calculations to the existing intelligence
    service and returns a structured analysis result.
    """

    def analyze(
        self,
        db: Session,
        portfolio_id: UUID,
        benchmark: str = "NIFTY50",
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:
        result = portfolio_intelligence_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            benchmark=benchmark,
            timeframe=timeframe,
            lookback_days=lookback_days,
        )

        return {
            "portfolio_id": str(portfolio_id),
            "intelligence_category": result.get(
                "intelligence_category"
            ),
            "overall_risk_score": result.get(
                "overall_risk_score"
            ),
            "risk_category": result.get("risk_category"),
            "portfolio_summary": result.get(
                "portfolio_summary", {}
            ),
            "risk": result.get("risk", {}),
            "portfolio_structure": result.get(
                "portfolio_structure", {}
            ),
            "risk_flags": result.get("risk_flags", []),
            "message": result.get("message"),
        }


portfolio_intelligence_agent = PortfolioIntelligenceAgent()
