from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_risk_score_service import (
    portfolio_risk_score_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioRiskDecompositionService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        benchmark: str = "NIFTY50",
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        risk_score = (
            portfolio_risk_score_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                benchmark=benchmark,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        components = risk_score.get(
            "risk_components",
            {}
        )

        if not components:
            return {
                "portfolio_id": portfolio_id,
                "benchmark": benchmark,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "overall_risk_score": None,
                "dominant_risk": None,
                "risk_components": {},
                "risk_contributions_pct": {},
                "risk_level": "Insufficient Data",
                "message": "No risk decomposition available",
            }

        component_values = {
            key: Decimal(str(value))
            for key, value in components.items()
        }

        dominant_risk = max(
            component_values,
            key=component_values.get,
        )

        total_component_score = sum(
            component_values.values(),
            Decimal("0"),
        )

        contributions = {}

        for name, value in component_values.items():
            if total_component_score > Decimal("0"):
                contribution = (
                    value
                    / total_component_score
                    * Decimal("100")
                )
            else:
                contribution = Decimal("0")

            contributions[name] = _round(
                contribution
            )

        dominant_value = component_values[
            dominant_risk
        ]

        if dominant_value >= Decimal("80"):
            risk_level = "Severe"
        elif dominant_value >= Decimal("60"):
            risk_level = "Elevated"
        elif dominant_value >= Decimal("40"):
            risk_level = "Moderate"
        else:
            risk_level = "Controlled"

        return {
            "portfolio_id": portfolio_id,
            "benchmark": benchmark,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "overall_risk_score":
                risk_score.get(
                    "overall_risk_score"
                ),
            "dominant_risk": dominant_risk,
            "risk_components": component_values,
            "risk_contributions_pct":
                contributions,
            "risk_level": risk_level,
            "message": None,
        }


portfolio_risk_decomposition_service = (
    PortfolioRiskDecompositionService()
)