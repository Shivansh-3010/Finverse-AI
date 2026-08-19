from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_performance_service import (
    portfolio_performance_service,
)
from services.portfolio_valuation_service import (
    portfolio_valuation_service,
)


class PortfolioSummaryService:
    """Combine portfolio valuation and performance metrics."""

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
    ) -> dict:

        valuation = (
            portfolio_valuation_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        performance = (
            portfolio_performance_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
            )
        )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,

            "positions": valuation["positions"],
            "position_count": len(
                valuation["positions"]
            ),

            "total_cost_basis": (
                valuation["total_cost_basis"]
            ),

            "total_market_value": (
                valuation["total_market_value"]
            ),

            "unrealized_pnl": (
                valuation["unrealized_pnl"]
            ),

            "unrealized_return_pct": (
                valuation["unrealized_return_pct"]
            ),

            "realized_pnl": (
                performance["realized_pnl"]
            ),

            "dividend_income": (
                performance["dividend_income"]
            ),

            "total_realized_return": (
                performance[
                    "total_realized_return"
                ]
            ),

            "total_bought": (
                performance["total_bought"]
            ),

            "total_sold": (
                performance["total_sold"]
            ),

            "net_cash_flow": (
                performance["net_cash_flow"]
            ),
        }


portfolio_summary_service = (
    PortfolioSummaryService()
)