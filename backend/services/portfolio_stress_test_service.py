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


class PortfolioStressTestService:
    """
    Portfolio-level deterministic stress testing.

    Supported scenarios:
        - market_shock
        - position_shock
        - volatility_shock
    """

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        scenario: str = "market_shock",
        shock_pct: Decimal = Decimal("-10"),
        symbol: str | None = None,
        timeframe: str = "1d",
    ) -> dict:

        scenario = scenario.lower().strip()

        allowed_scenarios = {
            "market_shock",
            "position_shock",
            "volatility_shock",
        }

        if scenario not in allowed_scenarios:
            raise ValueError(
                "Unsupported scenario. "
                "Supported scenarios: "
                "market_shock, position_shock, "
                "volatility_shock"
            )

        if shock_pct == Decimal("0"):
            raise ValueError(
                "shock_pct must not be zero"
            )

        exposure = (
            portfolio_exposure_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        positions = exposure["exposures"]
        total_market_value = Decimal(
            str(exposure["total_market_value"])
        )

        if not positions or total_market_value <= Decimal("0"):
            return {
                "portfolio_id": portfolio_id,
                "scenario": scenario,
                "shock_pct": shock_pct,
                "symbol": symbol,
                "timeframe": timeframe,
                "position_count": 0,
                "total_market_value": total_market_value,
                "estimated_pnl_impact": None,
                "estimated_return_impact_pct": None,
                "stressed_portfolio_value": None,
                "position_impacts": [],
                "risk_flags": [
                    "Portfolio has no active positions"
                ],
                "message": "Insufficient portfolio data",
            }

        position_impacts = []
        total_impact = Decimal("0")

        normalized_symbol = (
            symbol.upper().strip()
            if symbol
            else None
        )

        for position in positions:

            position_symbol = position["symbol"]

            market_value = Decimal(
                str(position["market_value"])
            )

            weight = (
                market_value / total_market_value
            )

            applied_shock = shock_pct

            if scenario == "position_shock":

                if (
                    normalized_symbol is not None
                    and position_symbol
                    == normalized_symbol
                ):
                    applied_shock = shock_pct
                else:
                    applied_shock = Decimal("0")

            elif scenario == "market_shock":

                applied_shock = shock_pct

            elif scenario == "volatility_shock":

                # Volatility shock is interpreted as
                # a proportional increase/decrease
                # in the portfolio's current exposure.
                applied_shock = shock_pct

            impact = (
                market_value
                * applied_shock
                / Decimal("100")
            )

            total_impact += impact

            position_impacts.append(
                {
                    "symbol": position_symbol,
                    "market_value": market_value,
                    "portfolio_weight_pct": _round(
                        weight * Decimal("100")
                    ),
                    "applied_shock_pct": _round(
                        applied_shock
                    ),
                    "estimated_pnl_impact": _round(
                        impact
                    ),
                    "estimated_return_impact_pct":
                        _round(
                            weight
                            * applied_shock
                        ),
                }
            )

        stressed_value = (
            total_market_value
            + total_impact
        )

        portfolio_return_impact = (
            total_impact
            / total_market_value
            * Decimal("100")
        )

        risk_flags = []

        if portfolio_return_impact <= Decimal("-10"):
            risk_flags.append(
                "Severe estimated portfolio loss"
            )
        elif portfolio_return_impact <= Decimal("-5"):
            risk_flags.append(
                "Material estimated portfolio loss"
            )
        elif portfolio_return_impact < Decimal("0"):
            risk_flags.append(
                "Portfolio experiences an estimated loss"
            )

        if scenario == "position_shock":
            if normalized_symbol is None:
                raise ValueError(
                    "symbol is required for "
                    "position_shock scenario"
                )

            matching_position = any(
                item["symbol"] == normalized_symbol
                for item in positions
            )

            if not matching_position:
                raise ValueError(
                    f"Symbol {normalized_symbol} "
                    "is not an active portfolio position"
                )

        if not risk_flags:
            risk_flags.append(
                "No major stress risk detected"
            )

        return {
            "portfolio_id": portfolio_id,
            "scenario": scenario,
            "shock_pct": _round(shock_pct),
            "symbol": normalized_symbol,
            "timeframe": timeframe,
            "position_count": len(positions),
            "total_market_value": total_market_value,
            "estimated_pnl_impact": _round(
                total_impact
            ),
            "estimated_return_impact_pct": _round(
                portfolio_return_impact
            ),
            "stressed_portfolio_value": _round(
                stressed_value
            ),
            "position_impacts": position_impacts,
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_stress_test_service = (
    PortfolioStressTestService()
)