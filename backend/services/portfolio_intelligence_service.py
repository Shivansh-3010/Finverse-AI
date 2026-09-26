from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_exposure_service import (
    portfolio_exposure_service,
)
from services.portfolio_factor_exposure_service import (
    portfolio_factor_exposure_service,
)
from services.portfolio_risk_score_service import (
    portfolio_risk_score_service,
)
from services.portfolio_drawdown_service import (
    portfolio_drawdown_service,
)
from services.portfolio_var_service import (
    portfolio_var_service,
)
from services.portfolio_liquidity_service import (
    portfolio_liquidity_service,
)
from services.portfolio_diversification_service import (
    portfolio_diversification_service,
)


class PortfolioIntelligenceService:
    """
    Aggregates the major portfolio analytics into a
    single portfolio intelligence view.

    This service is intentionally read-only.
    """

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        benchmark: str = "NIFTY50",
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        exposure = portfolio_exposure_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
        )

        factor_exposure = (
            portfolio_factor_exposure_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        risk_score = (
            portfolio_risk_score_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                benchmark=benchmark,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        drawdown = (
            portfolio_drawdown_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        var = portfolio_var_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
            lookback_days=lookback_days,
        )

        liquidity = (
            portfolio_liquidity_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        diversification = (
            portfolio_diversification_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        risk_flags = []

        for source in (
            risk_score,
            factor_exposure,
            drawdown,
            var,
            liquidity,
            diversification,
        ):
            for flag in source.get(
                "risk_flags",
                [],
            ):
                if flag not in risk_flags:
                    risk_flags.append(flag)

        overall_risk_score = risk_score.get(
            "overall_risk_score"
        )

        risk_category = risk_score.get(
            "risk_category"
        )

        if overall_risk_score is None:
            intelligence_category = (
                "Insufficient Data"
            )
        elif Decimal(
            str(overall_risk_score)
        ) >= Decimal("70"):
            intelligence_category = "High Risk"
        elif Decimal(
            str(overall_risk_score)
        ) >= Decimal("40"):
            intelligence_category = "Moderate Risk"
        else:
            intelligence_category = "Lower Risk"

        if not risk_flags:
            risk_flags.append(
                "No major portfolio risks detected"
            )

        return {
            "portfolio_id": portfolio_id,
            "benchmark": benchmark,
            "timeframe": timeframe,
            "lookback_days": lookback_days,

            "intelligence_category":
                intelligence_category,

            "overall_risk_score":
                overall_risk_score,

            "risk_category":
                risk_category,

            "portfolio_summary": {
                "position_count":
                    exposure.get(
                        "position_count"
                    ),
                "total_market_value":
                    exposure.get(
                        "total_market_value"
                    ),
                "largest_position":
                    exposure.get(
                        "largest_position"
                    ),
                "herfindahl_index":
                    exposure.get(
                        "herfindahl_index"
                    ),
            },

            "risk": {
                "risk_score":
                    risk_score,
                "drawdown":
                    drawdown,
                "var":
                    var,
            },

            "portfolio_structure": {
                "exposure":
                    exposure,
                "factor_exposure":
                    factor_exposure,
                "liquidity":
                    liquidity,
                "diversification":
                    diversification,
            },

            "risk_flags": risk_flags,

            "message": None,
        }


portfolio_intelligence_service = (
    PortfolioIntelligenceService()
)