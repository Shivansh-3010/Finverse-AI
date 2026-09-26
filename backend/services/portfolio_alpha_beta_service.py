from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_factor_exposure_service import (
    portfolio_factor_exposure_service,
)
from services.portfolio_benchmark_comparison_service import (
    portfolio_benchmark_comparison_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioAlphaBetaService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        benchmark: str = "NIFTY50",
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        comparison = (
            portfolio_benchmark_comparison_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                benchmark=benchmark,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        factor_exposure = (
            portfolio_factor_exposure_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        portfolio_return_raw = comparison.get(
            "portfolio_return_pct"
        )
        benchmark_return_raw = comparison.get(
            "benchmark_return_pct"
        )

        beta_raw = (
            factor_exposure
            .get("portfolio_factor_exposure", {})
            .get("market_beta")
        )

        if (
            portfolio_return_raw is None
            or benchmark_return_raw is None
            or beta_raw is None
        ):
            return {
                "portfolio_id": portfolio_id,
                "benchmark": benchmark,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "alpha_pct": None,
                "beta": None,
                "portfolio_return_pct":
                    portfolio_return_raw,
                "benchmark_return_pct":
                    benchmark_return_raw,
                "risk_characterization":
                    "Insufficient Data",
                "message": "Insufficient alpha/beta data",
            }

        portfolio_return = Decimal(
            str(portfolio_return_raw)
        )
        benchmark_return = Decimal(
            str(benchmark_return_raw)
        )
        beta = Decimal(str(beta_raw))

        expected_market_return = (
            beta * benchmark_return
        )

        alpha = (
            portfolio_return
            - expected_market_return
        )

        if beta > Decimal("1.10"):
            characterization = "Aggressive Market Exposure"
        elif beta < Decimal("0.90"):
            characterization = "Defensive Market Exposure"
        else:
            characterization = "Market-Like Exposure"

        return {
            "portfolio_id": portfolio_id,
            "benchmark": benchmark,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "alpha_pct": _round(alpha),
            "beta": _round(beta),
            "portfolio_return_pct":
                _round(portfolio_return),
            "benchmark_return_pct":
                _round(benchmark_return),
            "risk_characterization":
                characterization,
            "message": None,
        }


portfolio_alpha_beta_service = (
    PortfolioAlphaBetaService()
)