from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from repositories.ohlcv_repository import (
    OHLCVRepository,
)
from services.holding_service import (
    holding_service,
)

def _money(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def _percentage(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

class PortfolioValuationService:
    """Calculate portfolio market valuation from holdings and OHLCV data."""

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id,
        timeframe: str = "1d",
    ) -> dict:

        holdings = (
            holding_service.calculate_from_transactions(
                db,
                portfolio_id,
            )
        )

        ohlcv_repository = OHLCVRepository(db)

        positions = []

        total_cost_basis = Decimal("0")
        total_market_value = Decimal("0")

        for holding in holdings:

            symbol = holding["symbol"]
            quantity = holding["quantity"]
            avg_price = holding["avg_price"]
            cost_basis = holding["cost_basis"]

            candle = (
                ohlcv_repository.get_latest_candle(
                    symbol,
                    timeframe,
                )
            )

            if candle is None:
                continue

            current_price = _money(
                Decimal(str(candle.close))
            )

            market_value = _money(
                quantity * current_price
            )

            unrealized_pnl = _money(
                market_value - cost_basis
            )

            unrealized_return_pct = _percentage(
                (
                    (
                        unrealized_pnl
                        / cost_basis
                    )
                    * Decimal("100")
                )
                if cost_basis > Decimal("0")
                else Decimal("0")
            )

            total_cost_basis += cost_basis
            total_market_value += market_value

            positions.append(
                {
                    "symbol": symbol,
                    "quantity": quantity,
                    "avg_price": avg_price,
                    "cost_basis": cost_basis,
                    "current_price": current_price,
                    "market_value": market_value,
                    "unrealized_pnl": unrealized_pnl,
                    "unrealized_return_pct":
                        unrealized_return_pct,
                }
            )

        portfolio_unrealized_pnl = _money(
            total_market_value
            - total_cost_basis
        )

        portfolio_return_pct = _percentage(
            (
                (
                    portfolio_unrealized_pnl
                    / total_cost_basis
                )
                * Decimal("100")
            )
            if total_cost_basis > Decimal("0")
            else Decimal("0")
        )

        for position in positions:

            if total_market_value > Decimal("0"):

                position["portfolio_weight_pct"] = _percentage(
                    position["market_value"]
                    / total_market_value
                    * Decimal("100")
                )

            else:

                position["portfolio_weight_pct"] = (
                    Decimal("0")
                )
                
        total_cost_basis = _money(
            total_cost_basis
        )

        total_market_value = _money(
            total_market_value
        )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "positions": positions,
            "total_cost_basis": total_cost_basis,
            "total_market_value": total_market_value,
            "unrealized_pnl": portfolio_unrealized_pnl,
            "unrealized_return_pct":
                portfolio_return_pct,
        }


portfolio_valuation_service = (
    PortfolioValuationService()
)