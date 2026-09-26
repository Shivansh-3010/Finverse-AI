from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_exposure_service import (
    portfolio_exposure_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioScenarioAnalysisService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        scenario: str = "custom",
        shocks: dict[str, Decimal] | None = None,
        default_shock_pct: Decimal = Decimal("0"),
        timeframe: str = "1d",
    ) -> dict:

        exposure = portfolio_exposure_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
        )

        positions = exposure.get("exposures", [])

        total_market_value = Decimal(
            str(exposure.get("total_market_value", "0"))
        )

        if not positions or total_market_value <= Decimal("0"):
            return {
                "portfolio_id": portfolio_id,
                "scenario": scenario,
                "timeframe": timeframe,
                "position_count": 0,
                "total_market_value": total_market_value,
                "estimated_pnl_impact": Decimal("0"),
                "estimated_return_impact_pct": Decimal("0"),
                "stressed_portfolio_value": total_market_value,
                "position_impacts": [],
                "worst_affected_position": None,
                "scenario_category": "Insufficient Data",
                "risk_flags": [
                    "Portfolio has no active positions"
                ],
                "message": "Insufficient portfolio data",
            }

        normalized_shocks = {
            symbol.upper().strip(): Decimal(str(value))
            for symbol, value in (shocks or {}).items()
        }

        position_impacts = []
        total_pnl_impact = Decimal("0")

        for position in positions:

            symbol = position["symbol"]

            market_value = Decimal(
                str(position["market_value"])
            )

            portfolio_weight = (
                market_value
                / total_market_value
                * Decimal("100")
            )

            applied_shock = normalized_shocks.get(
                symbol,
                default_shock_pct,
            )

            pnl_impact = (
                market_value
                * applied_shock
                / Decimal("100")
            )

            portfolio_return_impact = (
                pnl_impact
                / total_market_value
                * Decimal("100")
            )

            total_pnl_impact += pnl_impact

            position_impacts.append(
                {
                    "symbol": symbol,
                    "market_value": market_value,
                    "portfolio_weight_pct": _round(
                        portfolio_weight
                    ),
                    "applied_shock_pct": _round(
                        applied_shock
                    ),
                    "estimated_pnl_impact": _round(
                        pnl_impact
                    ),
                    "estimated_return_impact_pct": _round(
                        portfolio_return_impact
                    ),
                }
            )

        stressed_value = (
            total_market_value
            + total_pnl_impact
        )

        portfolio_return_impact = (
            total_pnl_impact
            / total_market_value
            * Decimal("100")
        )

        position_impacts.sort(
            key=lambda item: item[
                "estimated_pnl_impact"
            ]
        )

        worst_position = (
            position_impacts[0]
            if position_impacts
            else None
        )

        absolute_return_impact = abs(
            portfolio_return_impact
        )

        if absolute_return_impact >= Decimal("20"):
            scenario_category = "Severe Impact"

        elif absolute_return_impact >= Decimal("10"):
            scenario_category = "High Impact"

        elif absolute_return_impact >= Decimal("5"):
            scenario_category = "Moderate Impact"

        elif absolute_return_impact > Decimal("0"):
            scenario_category = "Low Impact"

        else:
            scenario_category = "No Impact"

        risk_flags = []

        if portfolio_return_impact <= Decimal("-10"):
            risk_flags.append(
                "Scenario produces a severe estimated portfolio loss"
            )

        elif portfolio_return_impact <= Decimal("-5"):
            risk_flags.append(
                "Scenario produces a significant estimated portfolio loss"
            )

        if (
            worst_position is not None
            and worst_position[
                "estimated_pnl_impact"
            ] < Decimal("0")
        ):
            risk_flags.append(
                f"{worst_position['symbol']} has the largest "
                "negative scenario impact"
            )

        if len(normalized_shocks) > 1:
            risk_flags.append(
                "Scenario applies multiple position-specific shocks"
            )

        if not risk_flags:
            risk_flags.append(
                "No major scenario risks detected"
            )

        return {
            "portfolio_id": portfolio_id,
            "scenario": scenario,
            "timeframe": timeframe,
            "position_count": len(
                position_impacts
            ),
            "total_market_value": _round(
                total_market_value
            ),
            "estimated_pnl_impact": _round(
                total_pnl_impact
            ),
            "estimated_return_impact_pct": _round(
                portfolio_return_impact
            ),
            "stressed_portfolio_value": _round(
                stressed_value
            ),
            "position_impacts": position_impacts,
            "worst_affected_position": (
                worst_position["symbol"]
                if worst_position is not None
                else None
            ),
            "scenario_category": scenario_category,
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_scenario_analysis_service = (
    PortfolioScenarioAnalysisService()
)