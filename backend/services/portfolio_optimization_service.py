from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_exposure_service import (
    portfolio_exposure_service,
)
from services.portfolio_risk_score_service import (
    portfolio_risk_score_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioOptimizationService:
    """
    Produces a practical target-allocation recommendation.

    The first optimization layer is deliberately heuristic:
        - reduces excessive concentration
        - considers current portfolio weights
        - uses the existing portfolio risk score
        - preserves the existing investment universe

    It does not execute trades.
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

        risk_score = portfolio_risk_score_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            benchmark=benchmark,
            timeframe=timeframe,
            lookback_days=lookback_days,
        )

        positions = exposure.get("exposures", [])

        total_market_value = Decimal(
            str(exposure.get("total_market_value", "0"))
        )

        if not positions or total_market_value <= Decimal("0"):
            return {
                "portfolio_id": portfolio_id,
                "benchmark": benchmark,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "position_count": 0,
                "current_concentration_score": None,
                "optimized_concentration_score": None,
                "expected_risk_reduction_pct": None,
                "optimization_category": "Insufficient Data",
                "positions": [],
                "risk_flags": [
                    "Portfolio has no active positions"
                ],
                "message": "Insufficient portfolio data",
            }

        count = len(positions)

        current_weights = {
            item["symbol"]: Decimal(
                str(item["portfolio_weight_pct"])
            )
            for item in positions
        }

        # Equal-weight target is used as the neutral baseline.
        equal_weight = (
            Decimal("100")
            / Decimal(str(count))
        )

        # Cap individual positions at 40%.
        max_weight = Decimal("40")

        target_weights = {}

        for symbol, current_weight in current_weights.items():
            target_weights[symbol] = min(
                current_weight,
                max_weight,
            )

        remaining = (
            Decimal("100")
            - sum(target_weights.values())
        )

        # Redistribute remaining weight among positions
        # that are below the cap.
        while remaining > Decimal("0.01"):
            eligible = [
                symbol
                for symbol, weight in target_weights.items()
                if weight < max_weight
            ]

            if not eligible:
                break

            increment = (
                remaining
                / Decimal(str(len(eligible)))
            )

            distributed = Decimal("0")

            for symbol in eligible:
                capacity = (
                    max_weight
                    - target_weights[symbol]
                )

                addition = min(
                    increment,
                    capacity,
                    remaining - distributed,
                )

                if addition <= Decimal("0"):
                    continue

                target_weights[symbol] += addition
                distributed += addition

                if (
                    remaining - distributed
                    <= Decimal("0.01")
                ):
                    break

            if distributed <= Decimal("0"):
                break

            remaining -= distributed

        # For diversified portfolios, move slightly toward
        # equal weighting while respecting the 40% cap.
        for symbol in target_weights:
            target_weights[symbol] = (
                target_weights[symbol]
                + equal_weight
            ) / Decimal("2")

        # Normalize back to exactly 100%.
        target_total = sum(
            target_weights.values()
        )

        if target_total > Decimal("0"):
            for symbol in target_weights:
                target_weights[symbol] = (
                    target_weights[symbol]
                    / target_total
                    * Decimal("100")
                )

        current_hhi = sum(
            (
                weight / Decimal("100")
            ) ** 2
            for weight in current_weights.values()
        )

        optimized_hhi = sum(
            (
                weight / Decimal("100")
            ) ** 2
            for weight in target_weights.values()
        )

        current_concentration = (
            current_hhi * Decimal("10000")
        )

        optimized_concentration = (
            optimized_hhi * Decimal("10000")
        )

        concentration_reduction = (
            (
                current_concentration
                - optimized_concentration
            )
            / current_concentration
            * Decimal("100")
            if current_concentration > Decimal("0")
            else Decimal("0")
        )

        positions_result = []

        for item in positions:
            symbol = item["symbol"]

            current_weight = current_weights[symbol]
            target_weight = target_weights[symbol]

            change = (
                target_weight
                - current_weight
            )

            positions_result.append(
                {
                    "symbol": symbol,
                    "current_weight_pct": _round(
                        current_weight
                    ),
                    "target_weight_pct": _round(
                        target_weight
                    ),
                    "weight_change_pct": _round(
                        change
                    ),
                    "market_value": _round(
                        Decimal(
                            str(
                                item[
                                    "market_value"
                                ]
                            )
                        )
                    ),
                }
            )

        positions_result.sort(
            key=lambda item: abs(
                item["weight_change_pct"]
            ),
            reverse=True,
        )

        risk_score_value = risk_score.get(
            "overall_risk_score"
        )

        risk_score_value = (
            Decimal(str(risk_score_value))
            if risk_score_value is not None
            else None
        )

        if concentration_reduction >= Decimal("20"):
            optimization_category = "Strong Diversification Opportunity"
        elif concentration_reduction >= Decimal("5"):
            optimization_category = "Moderate Optimization Opportunity"
        else:
            optimization_category = "Minor Optimization Opportunity"

        risk_flags = []

        if concentration_reduction >= Decimal("5"):
            risk_flags.append(
                "Rebalancing can reduce portfolio concentration"
            )

        if risk_score_value is not None and risk_score_value >= Decimal("70"):
            risk_flags.append(
                "Current portfolio risk score is elevated"
            )

        largest_position = max(
            current_weights.values()
        )

        if largest_position > Decimal("50"):
            risk_flags.append(
                "Current allocation contains a position above 50%"
            )

        if not risk_flags:
            risk_flags.append(
                "No major allocation optimization risks detected"
            )

        return {
            "portfolio_id": portfolio_id,
            "benchmark": benchmark,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "position_count": count,
            "current_concentration_score": _round(
                current_concentration
            ),
            "optimized_concentration_score": _round(
                optimized_concentration
            ),
            "expected_risk_reduction_pct": _round(
                max(
                    concentration_reduction,
                    Decimal("0"),
                )
            ),
            "optimization_category": optimization_category,
            "positions": positions_result,
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_optimization_service = (
    PortfolioOptimizationService()
)