from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_drawdown_service import (
    portfolio_drawdown_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioRecoveryAnalysisService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        drawdown = portfolio_drawdown_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
            lookback_days=lookback_days,
        )

        current_drawdown_raw = drawdown.get(
            "current_drawdown_pct"
        )
        maximum_drawdown_raw = drawdown.get(
            "maximum_drawdown_pct"
        )
        duration_raw = drawdown.get(
            "drawdown_duration_days"
        )

        if current_drawdown_raw is None:
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "current_drawdown_pct": None,
                "maximum_drawdown_pct": None,
                "drawdown_duration_days": None,
                "estimated_recovery_return_pct": None,
                "recovery_status": "Insufficient Data",
                "recovery_category": "Insufficient Data",
                "risk_flags": [],
                "message": "Insufficient drawdown recovery data",
            }

        current_drawdown = Decimal(
            str(current_drawdown_raw)
        )

        maximum_drawdown = (
            Decimal(str(maximum_drawdown_raw))
            if maximum_drawdown_raw is not None
            else current_drawdown
        )

        duration_days = (
            int(duration_raw)
            if duration_raw is not None
            else 0
        )

        drawdown_magnitude = abs(current_drawdown)

        if drawdown_magnitude > Decimal("0"):
            estimated_recovery_return = (
                (
                    Decimal("100")
                    / (
                        Decimal("100")
                        - drawdown_magnitude
                    )
                )
                * Decimal("100")
                - Decimal("100")
            )
        else:
            estimated_recovery_return = Decimal("0")

        recovery_status = drawdown.get(
            "recovery_status",
            "Unknown",
        )

        if drawdown_magnitude >= Decimal("20"):
            recovery_category = "Severe Recovery Requirement"

        elif drawdown_magnitude >= Decimal("10"):
            recovery_category = "High Recovery Requirement"

        elif drawdown_magnitude >= Decimal("5"):
            recovery_category = "Moderate Recovery Requirement"

        elif drawdown_magnitude > Decimal("0"):
            recovery_category = "Minor Recovery Requirement"

        else:
            recovery_category = "No Recovery Required"

        risk_flags = []

        if drawdown_magnitude >= Decimal("10"):
            risk_flags.append(
                "Portfolio requires a significant return "
                "to recover from the current drawdown"
            )

        if duration_days >= 20:
            risk_flags.append(
                "Portfolio has remained in drawdown "
                "for an extended period"
            )

        if (
            maximum_drawdown is not None
            and abs(maximum_drawdown)
            >= Decimal("15")
        ):
            risk_flags.append(
                "Historical maximum drawdown is elevated"
            )

        if not risk_flags:
            risk_flags.append(
                "No major recovery risk detected"
            )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "current_drawdown_pct": _round(
                current_drawdown
            ),
            "maximum_drawdown_pct": _round(
                maximum_drawdown
            ),
            "drawdown_duration_days": duration_days,
            "estimated_recovery_return_pct": _round(
                estimated_recovery_return
            ),
            "recovery_status": recovery_status,
            "recovery_category": recovery_category,
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_recovery_analysis_service = (
    PortfolioRecoveryAnalysisService()
)