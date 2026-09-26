from decimal import Decimal, ROUND_HALF_UP
from math import sqrt
from uuid import UUID

from sqlalchemy.orm import Session

from repositories.ohlcv_repository import OHLCVRepository
from services.holding_service import holding_service
from services.benchmark_data_service import (
    benchmark_data_service,
)


def _decimal(value) -> Decimal:
    return Decimal(str(value))


def _round(value: Decimal, places: str = "0.01") -> Decimal:
    return value.quantize(
        Decimal(places),
        rounding=ROUND_HALF_UP,
    )


def _mean(values: list[Decimal]) -> Decimal:
    if not values:
        return Decimal("0")

    return (
        sum(values, Decimal("0"))
        / Decimal(len(values))
    )


def _variance(values: list[Decimal]) -> Decimal:
    if len(values) < 2:
        return Decimal("0")

    mean_value = _mean(values)

    total = Decimal("0")

    for value in values:
        difference = value - mean_value
        total += difference * difference

    return total / Decimal(len(values) - 1)


def _covariance(
    x: list[Decimal],
    y: list[Decimal],
) -> Decimal:

    if len(x) != len(y) or len(x) < 2:
        return Decimal("0")

    mean_x = _mean(x)
    mean_y = _mean(y)

    total = Decimal("0")

    for x_value, y_value in zip(x, y):
        total += (
            (x_value - mean_x)
            * (y_value - mean_y)
        )

    return total / Decimal(len(x) - 1)


def _annualized_volatility(
    returns: list[Decimal],
) -> Decimal | None:

    if len(returns) < 2:
        return None

    variance = _variance(returns)

    if variance <= Decimal("0"):
        return Decimal("0")

    volatility = Decimal(
        str(
            sqrt(
                float(variance)
            )
        )
    )

    return volatility * Decimal(
        str(sqrt(252))
    )


def _build_returns(
    prices: dict,
    common_dates: list,
) -> dict:

    returns = {}

    for previous_date, current_date in zip(
        common_dates,
        common_dates[1:],
    ):

        previous_price = prices.get(
            previous_date
        )

        current_price = prices.get(
            current_date
        )

        if (
            previous_price is None
            or current_price is None
            or previous_price <= Decimal("0")
        ):
            continue

        returns[current_date] = (
            current_price / previous_price
        ) - Decimal("1")

    return returns


class PortfolioFactorExposureService:
    """
    Calculate market-derived factor exposures
    for a portfolio.

    Current factors:

    - Market beta
    - Momentum
    - Realized volatility
    - Liquidity

    Fundamental factors such as value, growth,
    and quality are intentionally not calculated
    because the current market-data layer does
    not provide fundamental financial metrics.
    """

    DEFAULT_BENCHMARK = "NIFTY50"
    DEFAULT_TIMEFRAME = "1d"

    MOMENTUM_LOOKBACK = 63
    VOLATILITY_LOOKBACK = 63
    LIQUIDITY_LOOKBACK = 20

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        benchmark_symbol: str = DEFAULT_BENCHMARK,
        timeframe: str = DEFAULT_TIMEFRAME,
    ) -> dict:

        benchmark_symbol = (
            benchmark_symbol.upper()
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
            "benchmark": benchmark_symbol,
            "timeframe": timeframe,
        }

        if not holdings:
            return {
                **base_response,
                "position_count": 0,
                "portfolio_factor_exposure": None,
                "positions": [],
                "risk_flags": [
                    "Portfolio has no active positions"
                ],
                "message": (
                    "Portfolio has no holdings"
                ),
            }

        # ---------------------------------------------------------
        # Load benchmark history
        # ---------------------------------------------------------

        benchmark_records = (
            benchmark_data_service.get_history(
                benchmark_symbol,
                period="1y",
                interval=timeframe,
            )
        )

        benchmark_prices = {}

        for record in benchmark_records:

            timestamp = record["timestamp"]

            if timestamp.tzinfo is not None:
                timestamp = timestamp.replace(
                    tzinfo=None
                )

            benchmark_prices[
                timestamp.date()
            ] = _decimal(
                record["close"]
            )

        benchmark_dates = sorted(
            benchmark_prices.keys()
        )

        # ---------------------------------------------------------
        # Load position histories
        # ---------------------------------------------------------

        position_data = []

        total_market_value = Decimal("0")

        required_history = max(
            PortfolioFactorExposureService.MOMENTUM_LOOKBACK,
            PortfolioFactorExposureService.VOLATILITY_LOOKBACK,
            PortfolioFactorExposureService.LIQUIDITY_LOOKBACK,
        ) + 1

        for holding in holdings:

            symbol = holding["symbol"]

            records = (
                repository
                .get_latest_by_symbol_and_timeframe(
                    symbol,
                    timeframe,
                    limit=required_history,
                )
            )

            if len(records) < 2:
                continue

            prices = {}
            volumes = {}

            for record in records:

                timestamp = record.timestamp

                if timestamp.tzinfo is not None:
                    timestamp = timestamp.replace(
                        tzinfo=None
                    )

                date = timestamp.date()

                prices[date] = _decimal(
                    record.close
                )

                volumes[date] = _decimal(
                    record.volume or 0
                )

            dates = sorted(prices.keys())

            if len(dates) < 2:
                continue

            latest_date = dates[-1]

            latest_price = prices[
                latest_date
            ]

            quantity = _decimal(
                holding["quantity"]
            )

            market_value = (
                quantity * latest_price
            )

            if market_value <= Decimal("0"):
                continue

            position_data.append(
                {
                    "symbol": symbol,
                    "quantity": quantity,
                    "market_value": market_value,
                    "prices": prices,
                    "volumes": volumes,
                    "dates": dates,
                }
            )

            total_market_value += market_value

        if (
            not position_data
            or total_market_value <= Decimal("0")
        ):
            return {
                **base_response,
                "position_count": 0,
                "portfolio_factor_exposure": None,
                "positions": [],
                "risk_flags": [
                    "Unable to construct factor history"
                ],
                "message": (
                    "Unable to construct factor exposure"
                ),
            }

        # ---------------------------------------------------------
        # Portfolio weights
        # ---------------------------------------------------------

        for position in position_data:

            position["weight"] = (
                position["market_value"]
                / total_market_value
            )

        # ---------------------------------------------------------
        # Position-level factor calculations
        # ---------------------------------------------------------

        positions = []

        for position in position_data:

            symbol = position["symbol"]
            prices = position["prices"]
            volumes = position["volumes"]
            dates = position["dates"]
            weight = position["weight"]

            # -----------------------------------------------------
            # Momentum
            # -----------------------------------------------------

            momentum = None

            if len(dates) > (
                PortfolioFactorExposureService
                .MOMENTUM_LOOKBACK
            ):

                momentum_start = dates[
                    -(
                        PortfolioFactorExposureService
                        .MOMENTUM_LOOKBACK
                        + 1
                    )
                ]

                momentum_end = dates[-1]

                start_price = prices[
                    momentum_start
                ]

                end_price = prices[
                    momentum_end
                ]

                if start_price > Decimal("0"):

                    momentum = _round(
                        (
                            (
                                end_price
                                / start_price
                            )
                            - Decimal("1")
                        )
                        * Decimal("100")
                    )

            # -----------------------------------------------------
            # Volatility
            # -----------------------------------------------------

            volatility_returns = []

            volatility_dates = dates[
                -(
                    PortfolioFactorExposureService
                    .VOLATILITY_LOOKBACK
                    + 1
                ):
            ]

            for previous_date, current_date in zip(
                volatility_dates,
                volatility_dates[1:],
            ):

                previous_price = prices[
                    previous_date
                ]

                current_price = prices[
                    current_date
                ]

                if previous_price <= Decimal("0"):
                    continue

                volatility_returns.append(
                    (
                        current_price
                        / previous_price
                    )
                    - Decimal("1")
                )

            volatility = (
                _annualized_volatility(
                    volatility_returns
                )
                if volatility_returns
                else None
            )

            if volatility is not None:
                volatility = _round(
                    volatility
                    * Decimal("100")
                )

            # -----------------------------------------------------
            # Liquidity
            # -----------------------------------------------------

            liquidity_dates = dates[
                -PortfolioFactorExposureService
                .LIQUIDITY_LOOKBACK:
            ]

            dollar_volumes = []

            for date in liquidity_dates:

                price = prices.get(date)
                volume = volumes.get(date)

                if (
                    price is None
                    or volume is None
                    or price <= Decimal("0")
                    or volume <= Decimal("0")
                ):
                    continue

                dollar_volumes.append(
                    price * volume
                )

            average_daily_traded_value = None

            if dollar_volumes:

                average_daily_traded_value = _round(
                    _mean(dollar_volumes)
                )

            # -----------------------------------------------------
            # Position beta relative to benchmark
            # -----------------------------------------------------

            beta = None

            common_dates = sorted(
                set(dates)
                & set(benchmark_dates)
            )

            if len(common_dates) >= 3:

                asset_returns = _build_returns(
                    prices,
                    common_dates,
                )

                benchmark_returns = _build_returns(
                    benchmark_prices,
                    common_dates,
                )

                aligned_dates = sorted(
                    set(asset_returns.keys())
                    & set(
                        benchmark_returns.keys()
                    )
                )

                if len(aligned_dates) >= 2:

                    asset_return_values = [
                        asset_returns[date]
                        for date in aligned_dates
                    ]

                    benchmark_return_values = [
                        benchmark_returns[date]
                        for date in aligned_dates
                    ]

                    benchmark_variance = (
                        _variance(
                            benchmark_return_values
                        )
                    )

                    if benchmark_variance > Decimal("0"):

                        covariance = _covariance(
                            asset_return_values,
                            benchmark_return_values,
                        )

                        beta = _round(
                            covariance
                            / benchmark_variance
                        )

            positions.append(
                {
                    "symbol": symbol,
                    "portfolio_weight_pct": _round(
                        weight
                        * Decimal("100")
                    ),
                    "market_beta": beta,
                    "momentum_pct": momentum,
                    "realized_volatility_pct": (
                        volatility
                    ),
                    "average_daily_traded_value": (
                        average_daily_traded_value
                    ),
                }
            )

        # ---------------------------------------------------------
        # Portfolio weighted factor exposure
        # ---------------------------------------------------------

        weighted_beta = Decimal("0")
        weighted_momentum = Decimal("0")
        weighted_volatility = Decimal("0")

        beta_weight = Decimal("0")
        momentum_weight = Decimal("0")
        volatility_weight = Decimal("0")

        for position_data_item, position_result in zip(
            position_data,
            positions,
        ):

            weight = position_data_item[
                "weight"
            ]

            beta = position_result[
                "market_beta"
            ]

            momentum = position_result[
                "momentum_pct"
            ]

            volatility = position_result[
                "realized_volatility_pct"
            ]

            if beta is not None:

                weighted_beta += (
                    weight * beta
                )

                beta_weight += weight

            if momentum is not None:

                weighted_momentum += (
                    weight * momentum
                )

                momentum_weight += weight

            if volatility is not None:

                weighted_volatility += (
                    weight * volatility
                )

                volatility_weight += weight

        portfolio_beta = (
            weighted_beta / beta_weight
            if beta_weight > Decimal("0")
            else None
        )

        portfolio_momentum = (
            weighted_momentum
            / momentum_weight
            if momentum_weight > Decimal("0")
            else None
        )

        portfolio_volatility = (
            weighted_volatility
            / volatility_weight
            if volatility_weight > Decimal("0")
            else None
        )

        # ---------------------------------------------------------
        # Risk interpretation
        # ---------------------------------------------------------

        risk_flags = []

        if (
            portfolio_beta is not None
            and portfolio_beta >= Decimal("1.25")
        ):
            risk_flags.append(
                "Portfolio has high market sensitivity"
            )

        elif (
            portfolio_beta is not None
            and portfolio_beta <= Decimal("0.75")
        ):
            risk_flags.append(
                "Portfolio has below-market sensitivity"
            )

        if (
            portfolio_volatility is not None
            and portfolio_volatility >= Decimal("30")
        ):
            risk_flags.append(
                "Portfolio has high realized volatility"
            )

        if (
            portfolio_momentum is not None
            and portfolio_momentum <= Decimal("-10")
        ):
            risk_flags.append(
                "Portfolio has negative momentum exposure"
            )

        elif (
            portfolio_momentum is not None
            and portfolio_momentum >= Decimal("10")
        ):
            risk_flags.append(
                "Portfolio has positive momentum exposure"
            )

        if not risk_flags:
            risk_flags.append(
                "No major market-derived factor risks detected"
            )

        return {
            **base_response,
            "position_count": len(positions),
            "portfolio_factor_exposure": {
                "market_beta": (
                    _round(portfolio_beta)
                    if portfolio_beta is not None
                    else None
                ),
                "momentum_pct": (
                    _round(portfolio_momentum)
                    if portfolio_momentum is not None
                    else None
                ),
                "realized_volatility_pct": (
                    _round(
                        portfolio_volatility
                    )
                    if portfolio_volatility
                    is not None
                    else None
                ),
            },
            "positions": positions,
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_factor_exposure_service = (
    PortfolioFactorExposureService()
)