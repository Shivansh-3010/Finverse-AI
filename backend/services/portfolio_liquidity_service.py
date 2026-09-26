from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_exposure_service import (
    portfolio_exposure_service,
)
from services.portfolio_factor_exposure_service import (
    portfolio_factor_exposure_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioLiquidityService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
    ) -> dict:

        exposure = (
            portfolio_exposure_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        factor_exposure = (
            portfolio_factor_exposure_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        positions = exposure["exposures"]
        factor_positions = {
            item["symbol"]: item
            for item in factor_exposure.get(
                "positions",
                [],
            )
        }

        total_market_value = Decimal(
            str(exposure["total_market_value"])
        )

        if not positions or total_market_value <= Decimal("0"):
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "position_count": 0,
                "total_market_value": total_market_value,
                "portfolio_liquidity_score": None,
                "liquidity_category": "Insufficient Data",
                "estimated_daily_turnover_pct": None,
                "positions": [],
                "risk_flags": [
                    "Portfolio has no active positions"
                ],
                "message": "Insufficient liquidity data",
            }

        liquidity_positions = []
        weighted_liquidity = Decimal("0")
        risk_flags = []

        for position in positions:

            symbol = position["symbol"]

            market_value = Decimal(
                str(position["market_value"])
            )

            portfolio_weight = (
                market_value
                / total_market_value
                * Decimal("100")
            )

            factor = factor_positions.get(
                symbol,
                {},
            )

            traded_value_raw = factor.get(
                "average_daily_traded_value"
            )

            if traded_value_raw is None:
                average_daily_traded_value = Decimal("0")
            else:
                average_daily_traded_value = Decimal(
                    str(traded_value_raw)
                )

            if average_daily_traded_value > Decimal("0"):

                daily_turnover_pct = (
                    market_value
                    / average_daily_traded_value
                    * Decimal("100")
                )

                days_to_liquidate = (
                    market_value
                    / average_daily_traded_value
                )

            else:
                daily_turnover_pct = Decimal("0")
                days_to_liquidate = None

            if average_daily_traded_value <= Decimal("0"):
                liquidity_score = Decimal("0")

            elif days_to_liquidate <= Decimal("0.05"):
                liquidity_score = Decimal("100")

            elif days_to_liquidate <= Decimal("0.10"):
                liquidity_score = Decimal("90")

            elif days_to_liquidate <= Decimal("0.25"):
                liquidity_score = Decimal("75")

            elif days_to_liquidate <= Decimal("0.50"):
                liquidity_score = Decimal("60")

            elif days_to_liquidate <= Decimal("1.00"):
                liquidity_score = Decimal("40")

            elif days_to_liquidate <= Decimal("2.00"):
                liquidity_score = Decimal("25")

            else:
                liquidity_score = Decimal("10")

            weighted_liquidity += (
                liquidity_score
                * portfolio_weight
                / Decimal("100")
            )

            liquidity_positions.append(
                {
                    "symbol": symbol,
                    "market_value": market_value,
                    "portfolio_weight_pct": _round(
                        portfolio_weight
                    ),
                    "average_daily_traded_value":
                        _round(
                            average_daily_traded_value
                        ),
                    "daily_turnover_pct": _round(
                        daily_turnover_pct
                    ),
                    "estimated_days_to_liquidate":
                        _round(days_to_liquidate)
                        if days_to_liquidate is not None
                        else None,
                    "liquidity_score": _round(
                        liquidity_score
                    ),
                }
            )

            if (
                days_to_liquidate is not None
                and days_to_liquidate > Decimal("1")
            ):
                risk_flags.append(
                    f"{symbol} may require more than "
                    "one average trading day to liquidate"
                )

            if (
                portfolio_weight >= Decimal("25")
                and days_to_liquidate is not None
                and days_to_liquidate > Decimal("0.5")
            ):
                risk_flags.append(
                    f"{symbol} is a large position "
                    "with elevated liquidity risk"
                )

        portfolio_liquidity_score = _round(
            weighted_liquidity
        )

        weighted_daily_turnover = sum(
            (
                item["portfolio_weight_pct"]
                * item["daily_turnover_pct"]
                / Decimal("100")
                for item in liquidity_positions
            ),
            Decimal("0"),
        )

        weighted_daily_turnover = _round(
            weighted_daily_turnover
        )

        if portfolio_liquidity_score >= Decimal("80"):
            liquidity_category = "Highly Liquid"

        elif portfolio_liquidity_score >= Decimal("60"):
            liquidity_category = "Liquid"

        elif portfolio_liquidity_score >= Decimal("40"):
            liquidity_category = "Moderately Liquid"

        elif portfolio_liquidity_score >= Decimal("20"):
            liquidity_category = "Illiquid"

        else:
            liquidity_category = "Highly Illiquid"

        if (
            portfolio_liquidity_score < Decimal("40")
        ):
            risk_flags.append(
                "Portfolio has elevated liquidity risk"
            )

        if not risk_flags:
            risk_flags.append(
                "No major liquidity risks detected"
            )

        liquidity_positions.sort(
            key=lambda item: item["liquidity_score"]
        )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "position_count": len(
                liquidity_positions
            ),
            "total_market_value": total_market_value,
            "portfolio_liquidity_score":
                portfolio_liquidity_score,
            "liquidity_category":
                liquidity_category,
            "estimated_daily_turnover_pct":
                weighted_daily_turnover,
            "positions": liquidity_positions,
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_liquidity_service = (
    PortfolioLiquidityService()
)