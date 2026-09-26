from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_optimization_service import (
    portfolio_optimization_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioRebalancingService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        benchmark: str = "NIFTY50",
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        optimization = (
            portfolio_optimization_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                benchmark=benchmark,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        positions = optimization.get(
            "positions",
            []
        )

        if not positions:
            return {
                "portfolio_id": portfolio_id,
                "benchmark": benchmark,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "position_count": 0,
                "estimated_turnover_pct": None,
                "rebalancing_required": False,
                "positions": [],
                "message": "Insufficient portfolio data",
            }

        total_turnover = Decimal("0")
        rebalancing_positions = []

        for position in positions:

            change = Decimal(
                str(
                    position[
                        "weight_change_pct"
                    ]
                )
            )

            absolute_change = abs(change)

            total_turnover += absolute_change

            if absolute_change < Decimal("1"):
                action = "HOLD"
            elif change > Decimal("0"):
                action = "INCREASE"
            else:
                action = "REDUCE"

            rebalancing_positions.append(
                {
                    "symbol": position["symbol"],
                    "current_weight_pct":
                        position[
                            "current_weight_pct"
                        ],
                    "target_weight_pct":
                        position[
                            "target_weight_pct"
                        ],
                    "weight_change_pct":
                        position[
                            "weight_change_pct"
                        ],
                    "action": action,
                    "priority":
                        "HIGH"
                        if absolute_change >= Decimal("10")
                        else (
                            "MEDIUM"
                            if absolute_change >= Decimal("5")
                            else "LOW"
                        ),
                }
            )

        estimated_turnover = (
            total_turnover / Decimal("2")
        )

        rebalancing_required = any(
            abs(
                Decimal(
                    str(
                        item[
                            "weight_change_pct"
                        ]
                    )
                )
            ) >= Decimal("1")
            for item in rebalancing_positions
        )

        rebalancing_positions.sort(
            key=lambda item: abs(
                Decimal(
                    str(
                        item[
                            "weight_change_pct"
                        ]
                    )
                )
            ),
            reverse=True,
        )

        return {
            "portfolio_id": portfolio_id,
            "benchmark": benchmark,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "position_count": len(
                rebalancing_positions
            ),
            "estimated_turnover_pct": _round(
                estimated_turnover
            ),
            "rebalancing_required":
                rebalancing_required,
            "positions":
                rebalancing_positions,
            "message": None,
        }


portfolio_rebalancing_service = (
    PortfolioRebalancingService()
)