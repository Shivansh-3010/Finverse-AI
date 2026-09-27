from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_var_service import (
    portfolio_var_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioTailRiskService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        var_result = portfolio_var_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
            lookback_days=lookback_days,
        )

        var_95_raw = var_result.get("var_95_pct")
        var_99_raw = var_result.get("var_99_pct")
        es_95_raw = var_result.get(
            "expected_shortfall_95_pct"
        )
        es_99_raw = var_result.get(
            "expected_shortfall_99_pct"
        )

        if (
            var_95_raw is None
            or var_99_raw is None
            or es_95_raw is None
            or es_99_raw is None
        ):
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "var_95_pct": None,
                "var_99_pct": None,
                "expected_shortfall_95_pct": None,
                "expected_shortfall_99_pct": None,
                "tail_loss_premium_pct": None,
                "tail_risk_score": None,
                "tail_risk_category": "Insufficient Data",
                "risk_flags": [],
                "message": "Insufficient tail-risk data",
            }

        var_95 = Decimal(str(var_95_raw))
        var_99 = Decimal(str(var_99_raw))
        es_95 = Decimal(str(es_95_raw))
        es_99 = Decimal(str(es_99_raw))

        tail_loss_premium = es_99 - var_99

        if var_99 > Decimal("0"):
            tail_risk_ratio = (
                es_99 / var_99
            )
        else:
            tail_risk_ratio = Decimal("0")

        tail_risk_score = min(
            Decimal("100"),
            max(
                Decimal("0"),
                tail_risk_ratio * Decimal("50"),
            ),
        )

        risk_flags = []

        if es_99 > var_99:
            risk_flags.append(
                "Expected Shortfall exceeds 99% VaR"
            )

        if tail_loss_premium >= Decimal("1"):
            risk_flags.append(
                "Extreme-loss tail is materially larger "
                "than the 99% VaR threshold"
            )

        if tail_risk_score >= Decimal("75"):
            tail_risk_category = "Severe Tail Risk"

        elif tail_risk_score >= Decimal("50"):
            tail_risk_category = "High Tail Risk"

        elif tail_risk_score >= Decimal("25"):
            tail_risk_category = "Moderate Tail Risk"

        else:
            tail_risk_category = "Low Tail Risk"

        if not risk_flags:
            risk_flags.append(
                "No major tail-risk warning detected"
            )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "var_95_pct": _round(var_95),
            "var_99_pct": _round(var_99),
            "expected_shortfall_95_pct": _round(es_95),
            "expected_shortfall_99_pct": _round(es_99),
            "tail_loss_premium_pct": _round(
                tail_loss_premium
            ),
            "tail_risk_score": _round(
                tail_risk_score
            ),
            "tail_risk_category": tail_risk_category,
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_tail_risk_service = (
    PortfolioTailRiskService()
)