from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_valuation_service import (
    portfolio_valuation_service,
)


def _percentage(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioExposureService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
    ) -> dict:

        valuation = portfolio_valuation_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
        )

        positions = valuation["positions"]

        total_market_value = (
            valuation["total_market_value"]
        )

        exposures = []

        for position in positions:

            market_value = Decimal(
                str(position["market_value"])
            )

            weight = (
                market_value
                / total_market_value
                * Decimal("100")
                if total_market_value > Decimal("0")
                else Decimal("0")
            )

            exposures.append(
                {
                    "symbol": position["symbol"],
                    "market_value": market_value,
                    "portfolio_weight_pct": _percentage(
                        weight
                    ),
                    "unrealized_pnl": position[
                        "unrealized_pnl"
                    ],
                    "unrealized_return_pct": position[
                        "unrealized_return_pct"
                    ],
                }
            )

        exposures.sort(
            key=lambda item: item["portfolio_weight_pct"],
            reverse=True,
        )

        largest_position = (
            exposures[0]
            if exposures
            else None
        )

        hhi = sum(
            (
                item["portfolio_weight_pct"]
                * item["portfolio_weight_pct"]
                for item in exposures
            ),
            Decimal("0"),
        )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "position_count": len(exposures),
            "total_market_value": total_market_value,
            "largest_position": largest_position,
            "herfindahl_index": _percentage(hhi),
            "exposures": exposures,
            "message": None,
        }


portfolio_exposure_service = (
    PortfolioExposureService()
)