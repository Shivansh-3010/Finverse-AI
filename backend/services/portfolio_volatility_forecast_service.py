from decimal import Decimal, ROUND_HALF_UP
from statistics import mean, pstdev
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_performance_attribution_service import (
    portfolio_performance_attribution_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioVolatilityForecastService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        performance = (
            portfolio_performance_attribution_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        positions = performance.get("positions", [])

        if not positions:
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "historical_volatility_pct": None,
                "forecast_volatility_pct": None,
                "volatility_change_pct": None,
                "volatility_regime": "Insufficient Data",
                "message": "Insufficient portfolio return history",
            }

        returns = []

        for position in positions:
            return_pct = position.get("return_pct")

            if return_pct is not None:
                returns.append(
                    float(Decimal(str(return_pct)))
                )

        if len(returns) < 2:
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "historical_volatility_pct": None,
                "forecast_volatility_pct": None,
                "volatility_change_pct": None,
                "volatility_regime": "Insufficient Data",
                "message": "Insufficient return observations",
            }

        historical_volatility = Decimal(
            str(pstdev(returns))
        )

        recent_window = returns[
            max(0, len(returns) // 2):
        ]

        recent_volatility = Decimal(
            str(pstdev(recent_window))
        ) if len(recent_window) >= 2 else historical_volatility

        forecast_volatility = (
            historical_volatility * Decimal("0.40")
            + recent_volatility * Decimal("0.60")
        )

        if historical_volatility > Decimal("0"):
            volatility_change = (
                (
                    forecast_volatility
                    - historical_volatility
                )
                / historical_volatility
                * Decimal("100")
            )
        else:
            volatility_change = Decimal("0")

        if forecast_volatility >= Decimal("5"):
            regime = "Very High Volatility"

        elif forecast_volatility >= Decimal("3"):
            regime = "High Volatility"

        elif forecast_volatility >= Decimal("1.5"):
            regime = "Moderate Volatility"

        else:
            regime = "Low Volatility"

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "historical_volatility_pct": _round(
                historical_volatility
            ),
            "forecast_volatility_pct": _round(
                forecast_volatility
            ),
            "volatility_change_pct": _round(
                volatility_change
            ),
            "volatility_regime": regime,
            "message": None,
        }


portfolio_volatility_forecast_service = (
    PortfolioVolatilityForecastService()
)