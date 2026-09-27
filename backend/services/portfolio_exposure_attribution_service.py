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


class PortfolioExposureAttributionService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
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
                "timeframe": timeframe,
                "position_count": 0,
                "total_market_value": total_market_value,
                "positive_exposure_pct": Decimal("0"),
                "negative_exposure_pct": Decimal("0"),
                "net_exposure_pct": Decimal("0"),
                "largest_exposure_symbol": None,
                "largest_exposure_pct": None,
                "positions": [],
                "message": "No active portfolio exposures",
            }

        attribution_positions = []
        positive_exposure = Decimal("0")
        negative_exposure = Decimal("0")
        largest_symbol = None
        largest_weight = Decimal("0")

        for position in positions:
            symbol = position["symbol"]

            market_value = Decimal(
                str(position["market_value"])
            )

            weight_pct = (
                market_value
                / total_market_value
                * Decimal("100")
            )

            if weight_pct >= Decimal("0"):
                positive_exposure += weight_pct
            else:
                negative_exposure += abs(weight_pct)

            if abs(weight_pct) > largest_weight:
                largest_weight = abs(weight_pct)
                largest_symbol = symbol

            attribution_positions.append(
                {
                    "symbol": symbol,
                    "market_value": market_value,
                    "exposure_pct": _round(weight_pct),
                    "absolute_exposure_pct": _round(
                        abs(weight_pct)
                    ),
                }
            )

        net_exposure = positive_exposure - negative_exposure

        attribution_positions.sort(
            key=lambda item: item["absolute_exposure_pct"],
            reverse=True,
        )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "position_count": len(attribution_positions),
            "total_market_value": total_market_value,
            "positive_exposure_pct": _round(
                positive_exposure
            ),
            "negative_exposure_pct": _round(
                negative_exposure
            ),
            "net_exposure_pct": _round(net_exposure),
            "largest_exposure_symbol": largest_symbol,
            "largest_exposure_pct": _round(
                largest_weight
            ),
            "positions": attribution_positions,
            "message": None,
        }


portfolio_exposure_attribution_service = (
    PortfolioExposureAttributionService()
)