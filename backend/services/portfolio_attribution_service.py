from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from repositories.ohlcv_repository import OHLCVRepository
from services.holding_service import holding_service


class PortfolioAttributionService:
    """
    Calculates holding-level portfolio return and P&L contribution.

    Contribution is based on:
        holding weight × holding return

    The service uses cost-basis weights so attribution remains
    deterministic even when current market values are unavailable.
    """

    def __init__(self) -> None:
        self.ohlcv_repository = OHLCVRepository

    @staticmethod
    def _decimal(value: Any) -> Decimal:
        if value is None:
            return Decimal("0")

        return Decimal(str(value))

    @staticmethod
    def _round(value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"))

    def _get_prices(
        self,
        db: Session,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> list[Any]:
        return (
            self.ohlcv_repository(db)
            .get_history_by_symbol_and_timeframe_between(
                symbol,
                timeframe,
                start,
                end,
            )
        )

    def calculate(
        self,
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict[str, Any]:
        holdings = holding_service.calculate_from_transactions(
            db,
            portfolio_id,
        )

        end = datetime.now(timezone.utc)
        start = end - timedelta(days=lookback_days)

        if not holdings:
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "position_count": 0,
                "total_cost_basis": Decimal("0.00"),
                "portfolio_return": None,
                "total_pnl_contribution": Decimal("0.00"),
                "positions": [],
                "message": "Portfolio has no holdings",
            }

        total_cost_basis = sum(
            (
                self._decimal(h["cost_basis"])
                for h in holdings
            ),
            Decimal("0"),
        )

        if total_cost_basis <= 0:
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "position_count": len(holdings),
                "total_cost_basis": Decimal("0.00"),
                "portfolio_return": None,
                "total_pnl_contribution": Decimal("0.00"),
                "positions": [],
                "message": "Portfolio has no positive cost basis",
            }

        positions = []
        total_contribution = Decimal("0")

        for holding in holdings:
            symbol = holding["symbol"]
            quantity = self._decimal(holding["quantity"])
            avg_price = self._decimal(holding["avg_price"])
            cost_basis = self._decimal(holding["cost_basis"])

            rows = self._get_prices(
                db,
                symbol,
                timeframe,
                start,
                end,
            )

            valid_rows = [
                row
                for row in rows
                if row.close is not None
            ]

            if len(valid_rows) < 2:
                positions.append(
                    {
                        "symbol": symbol,
                        "quantity": quantity,
                        "cost_basis": self._round(cost_basis),
                        "portfolio_weight_pct": self._round(
                            cost_basis / total_cost_basis * 100
                        ),
                        "start_price": None,
                        "end_price": None,
                        "return_pct": None,
                        "pnl": None,
                        "return_contribution_pct": None,
                        "message": "Insufficient price history",
                    }
                )
                continue

            first_price = self._decimal(
                valid_rows[0].close
            )
            last_price = self._decimal(
                valid_rows[-1].close
            )

            if first_price <= 0:
                positions.append(
                    {
                        "symbol": symbol,
                        "quantity": quantity,
                        "cost_basis": self._round(cost_basis),
                        "portfolio_weight_pct": self._round(
                            cost_basis / total_cost_basis * 100
                        ),
                        "start_price": None,
                        "end_price": None,
                        "return_pct": None,
                        "pnl": None,
                        "return_contribution_pct": None,
                        "message": "Invalid starting price",
                    }
                )
                continue

            holding_return = (
                last_price / first_price
            ) - Decimal("1")

            pnl = quantity * (
                last_price - first_price
            )

            weight = cost_basis / total_cost_basis

            contribution = weight * holding_return

            total_contribution += contribution

            positions.append(
                {
                    "symbol": symbol,
                    "quantity": quantity,
                    "cost_basis": self._round(cost_basis),
                    "portfolio_weight_pct": self._round(
                        weight * 100
                    ),
                    "start_price": self._round(first_price),
                    "end_price": self._round(last_price),
                    "return_pct": self._round(
                        holding_return * 100
                    ),
                    "pnl": self._round(pnl),
                    "return_contribution_pct": self._round(
                        contribution * 100
                    ),
                    "message": None,
                }
            )

        valid_positions = [
            position
            for position in positions
            if position["return_contribution_pct"] is not None
        ]

        portfolio_return = (
            sum(
                (
                    position["return_contribution_pct"]
                    for position in valid_positions
                ),
                Decimal("0"),
            )
        )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "position_count": len(holdings),
            "total_cost_basis": self._round(
                total_cost_basis
            ),
            "portfolio_return": self._round(
                portfolio_return
            ),
            "total_pnl_contribution": self._round(
                total_contribution
                * total_cost_basis
            ),
            "positions": positions,
            "message": None,
        }


portfolio_attribution_service = PortfolioAttributionService()