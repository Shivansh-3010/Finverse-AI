from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from services.holding_service import holding_service
from repositories.ohlcv_repository import OHLCVRepository


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioPerformanceAttributionService:
    """
    Explains portfolio return and P&L contribution
    by individual position.

    Attribution is based on:
        - transaction-derived cost basis
        - historical start/end prices
        - current portfolio weights
    """

    def __init__(self) -> None:
        self.ohlcv_repository = OHLCVRepository

    def calculate(
        self,
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        holdings = (
            holding_service.calculate_from_transactions(
                db,
                portfolio_id,
            )
        )

        if not holdings:
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "position_count": 0,
                "total_cost_basis": Decimal("0"),
                "portfolio_return": None,
                "total_pnl_contribution": Decimal("0"),
                "positions": [],
                "message": "Portfolio has no active positions",
            }

        end = datetime.now(timezone.utc)
        start = (
            end
            - timedelta(days=lookback_days)
        )

        total_cost_basis = sum(
            (
                Decimal(
                    str(item["cost_basis"])
                )
                for item in holdings
            ),
            Decimal("0"),
        )

        if total_cost_basis <= Decimal("0"):
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "position_count": 0,
                "total_cost_basis": Decimal("0"),
                "portfolio_return": None,
                "total_pnl_contribution": Decimal("0"),
                "positions": [],
                "message": "Invalid portfolio cost basis",
            }

        results = []
        total_pnl = Decimal("0")

        for holding in holdings:

            symbol = holding["symbol"]

            rows = (
                self.ohlcv_repository(db)
                .get_history_by_symbol_and_timeframe_between(
                    symbol,
                    timeframe,
                    start,
                    end,
                )
            )

            if not rows:
                continue

            valid_rows = [
                row
                for row in rows
                if row.close is not None
            ]

            if len(valid_rows) < 2:
                continue

            valid_rows.sort(
                key=lambda row: row.timestamp
            )

            start_price = Decimal(
                str(valid_rows[0].close)
            )

            end_price = Decimal(
                str(valid_rows[-1].close)
            )

            quantity = Decimal(
                str(holding["quantity"])
            )

            cost_basis = Decimal(
                str(holding["cost_basis"])
            )

            if start_price <= Decimal("0"):
                continue

            return_pct = (
                (
                    end_price
                    / start_price
                )
                - Decimal("1")
            ) * Decimal("100")

            pnl = (
                end_price
                - start_price
            ) * quantity

            portfolio_weight = (
                cost_basis
                / total_cost_basis
                * Decimal("100")
            )

            return_contribution = (
                return_pct
                * portfolio_weight
                / Decimal("100")
            )

            total_pnl += pnl

            results.append(
                {
                    "symbol": symbol,
                    "quantity": quantity,
                    "cost_basis": _round(
                        cost_basis
                    ),
                    "portfolio_weight_pct": _round(
                        portfolio_weight
                    ),
                    "start_price": _round(
                        start_price
                    ),
                    "end_price": _round(
                        end_price
                    ),
                    "return_pct": _round(
                        return_pct
                    ),
                    "pnl": _round(
                        pnl
                    ),
                    "return_contribution_pct": _round(
                        return_contribution
                    ),
                    "message": None,
                }
            )

        if not results:
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "position_count": 0,
                "total_cost_basis": _round(
                    total_cost_basis
                ),
                "portfolio_return": None,
                "total_pnl_contribution": Decimal("0"),
                "positions": [],
                "message": "Insufficient price history",
            }

        portfolio_return = sum(
            (
                item["return_contribution_pct"]
                for item in results
            ),
            Decimal("0"),
        )

        results.sort(
            key=lambda item: item[
                "return_contribution_pct"
            ],
            reverse=True,
        )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "position_count": len(results),
            "total_cost_basis": _round(
                total_cost_basis
            ),
            "portfolio_return": _round(
                portfolio_return
            ),
            "total_pnl_contribution": _round(
                total_pnl
            ),
            "positions": results,
            "message": None,
        }


portfolio_performance_attribution_service = (
    PortfolioPerformanceAttributionService()
)