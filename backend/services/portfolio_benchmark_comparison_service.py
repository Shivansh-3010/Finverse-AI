from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_performance_attribution_service import (
    portfolio_performance_attribution_service,
)
from repositories.ohlcv_repository import OHLCVRepository


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioBenchmarkComparisonService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        benchmark: str = "NIFTY50",
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        attribution = (
            portfolio_performance_attribution_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        portfolio_return_raw = attribution.get(
            "portfolio_return"
        )

        if portfolio_return_raw is None:
            return {
                "portfolio_id": portfolio_id,
                "benchmark": benchmark,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "portfolio_return_pct": None,
                "benchmark_return_pct": None,
                "excess_return_pct": None,
                "relative_performance": "Insufficient Data",
                "message": "Insufficient portfolio return data",
            }

        end = datetime.now(timezone.utc)
        start = end - timedelta(days=lookback_days)

        rows = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe_between(
                benchmark,
                timeframe,
                start,
                end,
            )
        )

        valid_rows = [
            row
            for row in rows
            if row.close is not None
        ]

        if len(valid_rows) < 2:
            return {
                "portfolio_id": portfolio_id,
                "benchmark": benchmark,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "portfolio_return_pct": _round(
                    Decimal(str(portfolio_return_raw))
                ),
                "benchmark_return_pct": None,
                "excess_return_pct": None,
                "relative_performance": "Insufficient Data",
                "message": "Insufficient benchmark history",
            }

        valid_rows.sort(
            key=lambda row: row.timestamp
        )

        start_price = Decimal(
            str(valid_rows[0].close)
        )
        end_price = Decimal(
            str(valid_rows[-1].close)
        )

        if start_price <= Decimal("0"):
            benchmark_return = Decimal("0")
        else:
            benchmark_return = (
                (
                    end_price / start_price
                )
                - Decimal("1")
            ) * Decimal("100")

        portfolio_return = Decimal(
            str(portfolio_return_raw)
        )

        excess_return = (
            portfolio_return
            - benchmark_return
        )

        if excess_return > Decimal("1"):
            relative_performance = "Outperforming"
        elif excess_return < Decimal("-1"):
            relative_performance = "Underperforming"
        else:
            relative_performance = "In Line"

        return {
            "portfolio_id": portfolio_id,
            "benchmark": benchmark,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "portfolio_return_pct": _round(
                portfolio_return
            ),
            "benchmark_return_pct": _round(
                benchmark_return
            ),
            "excess_return_pct": _round(
                excess_return
            ),
            "relative_performance": relative_performance,
            "message": None,
        }


portfolio_benchmark_comparison_service = (
    PortfolioBenchmarkComparisonService()
)