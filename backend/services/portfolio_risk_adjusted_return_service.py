from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_performance_attribution_service import (
    portfolio_performance_attribution_service,
)
from services.portfolio_var_service import (
    portfolio_var_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioRiskAdjustedReturnService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
        risk_free_rate_pct: Decimal = Decimal("0"),
    ) -> dict:

        attribution = (
            portfolio_performance_attribution_service.calculate(
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

        portfolio_return_raw = attribution.get(
            "portfolio_return"
        )

        var_raw = var.get("var_95_pct")

        if (
            portfolio_return_raw is None
            or var_raw is None
        ):
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "portfolio_return_pct": None,
                "risk_free_rate_pct":
                    risk_free_rate_pct,
                "downside_risk_pct": None,
                "risk_adjusted_return": None,
                "performance_category":
                    "Insufficient Data",
                "message":
                    "Insufficient risk-adjusted return data",
            }

        portfolio_return = Decimal(
            str(portfolio_return_raw)
        )
        downside_risk = Decimal(
            str(var_raw)
        )

        excess_return = (
            portfolio_return
            - risk_free_rate_pct
        )

        if downside_risk > Decimal("0"):
            risk_adjusted_return = (
                excess_return
                / downside_risk
            )
        else:
            risk_adjusted_return = Decimal("0")

        if risk_adjusted_return >= Decimal("1"):
            category = "Strong Risk-Adjusted Performance"
        elif risk_adjusted_return >= Decimal("0.5"):
            category = "Acceptable Risk-Adjusted Performance"
        elif risk_adjusted_return >= Decimal("0"):
            category = "Weak Risk-Adjusted Performance"
        else:
            category = "Poor Risk-Adjusted Performance"

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "portfolio_return_pct":
                _round(portfolio_return),
            "risk_free_rate_pct":
                _round(risk_free_rate_pct),
            "downside_risk_pct":
                _round(downside_risk),
            "risk_adjusted_return":
                _round(risk_adjusted_return),
            "performance_category": category,
            "message": None,
        }


portfolio_risk_adjusted_return_service = (
    PortfolioRiskAdjustedReturnService()
)