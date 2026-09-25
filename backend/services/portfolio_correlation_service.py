from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from repositories.ohlcv_repository import OHLCVRepository
from services.holding_service import holding_service


def _decimal(value) -> Decimal:
    return Decimal(str(value))


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.0001"),
        rounding=ROUND_HALF_UP,
    )


def _correlation(
    x: list[Decimal],
    y: list[Decimal],
) -> Decimal | None:

    if len(x) != len(y) or len(x) < 2:
        return None

    mean_x = sum(x, Decimal("0")) / Decimal(len(x))
    mean_y = sum(y, Decimal("0")) / Decimal(len(y))

    covariance = Decimal("0")
    variance_x = Decimal("0")
    variance_y = Decimal("0")

    for x_value, y_value in zip(x, y):

        dx = x_value - mean_x
        dy = y_value - mean_y

        covariance += dx * dy
        variance_x += dx * dx
        variance_y += dy * dy

    if variance_x <= Decimal("0") or variance_y <= Decimal("0"):
        return None

    return covariance / (
        variance_x.sqrt() * variance_y.sqrt()
    )


class PortfolioCorrelationService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        if lookback_days < 2:
            raise ValueError(
                "lookback_days must be at least 2"
            )

        repository = OHLCVRepository(db)

        holdings = (
            holding_service.calculate_from_transactions(
                db,
                portfolio_id,
            )
        )

        base_response = {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
        }

        if len(holdings) < 2:
            return {
                **base_response,
                "symbols": [],
                "observation_count": 0,
                "matrix": {},
                "message": (
                    "At least two holdings are required"
                ),
            }

        symbol_prices = {}

        for holding in holdings:

            symbol = holding["symbol"]

            records = (
                repository.get_latest_by_symbol_and_timeframe(
                    symbol,
                    timeframe,
                    limit=lookback_days + 1,
                )
            )

            if len(records) < 2:
                continue

            prices = {}

            for record in records:

                timestamp = record.timestamp

                if timestamp.tzinfo is not None:
                    timestamp = timestamp.replace(
                        tzinfo=None
                    )

                prices[timestamp.date()] = _decimal(
                    record.close
                )

            if len(prices) >= 2:
                symbol_prices[symbol] = prices

        symbols = sorted(symbol_prices.keys())

        if len(symbols) < 2:
            return {
                **base_response,
                "symbols": symbols,
                "observation_count": 0,
                "matrix": {},
                "message": (
                    "Insufficient history for correlation"
                ),
            }

        return_series = {}

        for symbol in symbols:

            prices = symbol_prices[symbol]
            dates = sorted(prices.keys())

            returns = {}

            for previous_date, current_date in zip(
                dates,
                dates[1:],
            ):

                previous_price = prices[previous_date]
                current_price = prices[current_date]

                if previous_price <= Decimal("0"):
                    continue

                returns[current_date] = (
                    current_price / previous_price
                ) - Decimal("1")

            return_series[symbol] = returns

        common_dates = None

        for symbol in symbols:

            dates = set(
                return_series[symbol].keys()
            )

            if common_dates is None:
                common_dates = dates
            else:
                common_dates &= dates

        common_dates = sorted(
            common_dates or set()
        )

        if len(common_dates) < 2:
            return {
                **base_response,
                "symbols": symbols,
                "observation_count": len(
                    common_dates
                ),
                "matrix": {},
                "message": (
                    "Insufficient common observations"
                ),
            }

        matrix = {}

        for symbol_x in symbols:

            matrix[symbol_x] = {}

            x_returns = [
                return_series[symbol_x][date]
                for date in common_dates
            ]

            for symbol_y in symbols:

                y_returns = [
                    return_series[symbol_y][date]
                    for date in common_dates
                ]

                correlation = _correlation(
                    x_returns,
                    y_returns,
                )

                matrix[symbol_x][symbol_y] = (
                    _round(correlation)
                    if correlation is not None
                    else None
                )

        return {
            **base_response,
            "symbols": symbols,
            "observation_count": len(common_dates),
            "matrix": matrix,
            "message": None,
        }


portfolio_correlation_service = (
    PortfolioCorrelationService()
)