from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from repositories.ohlcv_repository import OHLCVRepository
from services.holding_service import holding_service
from services.benchmark_data_service import benchmark_data_service


def _percent(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def _decimal(value) -> Decimal:
    return Decimal(str(value))


def _mean(values: list[Decimal]) -> Decimal:
    if not values:
        return Decimal("0")

    return sum(values, Decimal("0")) / Decimal(len(values))


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


def _variance(values: list[Decimal]) -> Decimal:

    if len(values) < 2:
        return Decimal("0")

    mean_value = _mean(values)

    total = Decimal("0")

    for value in values:
        difference = value - mean_value
        total += difference * difference

    return total / Decimal(len(values) - 1)


class PortfolioBetaService:
    """
    Calculate portfolio beta relative to a benchmark.

    Beta = Cov(Rp, Rm) / Var(Rm)

    Rp = portfolio returns
    Rm = benchmark returns
    """

    DEFAULT_BENCHMARK = "NIFTY50"
    DEFAULT_TIMEFRAME = "1d"
    DEFAULT_LOOKBACK_DAYS = 365

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        benchmark_symbol: str = DEFAULT_BENCHMARK,
        timeframe: str = DEFAULT_TIMEFRAME,
        lookback_days: int = DEFAULT_LOOKBACK_DAYS,
    ) -> dict:

        if lookback_days < 2:
            raise ValueError(
                "lookback_days must be at least 2"
            )

        benchmark_symbol = benchmark_symbol.upper()

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
            "lookback_days": lookback_days,
        }

        if not holdings:
            return {
                **base_response,
                "beta": None,
                "observation_count": 0,
                "message": "Portfolio has no holdings",
            }

        start_date = (
            datetime.now(timezone.utc)
            - timedelta(days=lookback_days)
        )

        end_date = datetime.now(timezone.utc)

        # ---------------------------------------------------------
        # Benchmark data
        # ---------------------------------------------------------

        benchmark_records = (
            benchmark_data_service.get_history(
                benchmark_symbol,
                period=f"{lookback_days}d",
                interval=timeframe,
            )
        )

        if len(benchmark_records) < 3:

            return {
                **base_response,
                "beta": None,
                "observation_count": 0,
                "message": (
                    "Insufficient benchmark history"
                ),
            }

        benchmark_prices = {}

        for record in benchmark_records:

            timestamp = record["timestamp"]

            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(
                    tzinfo=timezone.utc
                )

            benchmark_prices[timestamp.date()] = _decimal(
                record["close"]
            )

        benchmark_timestamps = sorted(
            benchmark_prices.keys()
        )

        # ---------------------------------------------------------
        # Portfolio holdings
        # ---------------------------------------------------------

        holding_data = []

        total_market_value = Decimal("0")

        for holding in holdings:

            symbol = holding["symbol"]

            records = (
                repository
                .get_history_by_symbol_and_timeframe_between(
                    symbol,
                    timeframe,
                    start_date,
                    end_date,
                )
            )

            if len(records) < 2:
                continue

            prices = {}

            for record in records:

                timestamp = record.timestamp

                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(
                        tzinfo=timezone.utc
                    )

                prices[timestamp.date()] = _decimal(
                    record.close
                )

            common_timestamps = sorted(
                set(prices.keys())
                & set(benchmark_prices.keys())
            )

            if len(common_timestamps) < 2:
                continue

            latest_price = prices[
                common_timestamps[-1]
            ]

            quantity = _decimal(
                holding["quantity"]
            )

            market_value = (
                quantity * latest_price
            )

            if market_value <= Decimal("0"):
                continue

            holding_data.append(
                {
                    "symbol": symbol,
                    "prices": prices,
                    "timestamps": common_timestamps,
                    "market_value": market_value,
                }
            )

            total_market_value += market_value

        if (
            not holding_data
            or total_market_value <= Decimal("0")
        ):

            return {
                **base_response,
                "beta": None,
                "observation_count": 0,
                "message": (
                    "Unable to construct portfolio returns"
                ),
            }

        # ---------------------------------------------------------
        # Portfolio weights
        # ---------------------------------------------------------

        weights = {
            item["symbol"]:
                item["market_value"]
                / total_market_value
            for item in holding_data
        }

        # ---------------------------------------------------------
        # Common dates
        # ---------------------------------------------------------

        common_dates = set(
            benchmark_timestamps
        )

        for item in holding_data:

            common_dates &= set(
                item["timestamps"]
            )

        common_dates = sorted(common_dates)

        if len(common_dates) < 3:

            return {
                **base_response,
                "beta": None,
                "observation_count": 0,
                "message": (
                    "Insufficient common observations"
                ),
            }

        # ---------------------------------------------------------
        # Build aligned return series
        # ---------------------------------------------------------

        portfolio_returns = []

        aligned_benchmark_returns = []

        for previous_date, current_date in zip(
            common_dates,
            common_dates[1:],
        ):

            portfolio_return = Decimal("0")

            valid_weight = Decimal("0")

            for item in holding_data:

                previous_price = item["prices"].get(
                    previous_date
                )

                current_price = item["prices"].get(
                    current_date
                )

                if (
                    previous_price is None
                    or current_price is None
                    or previous_price <= Decimal("0")
                ):
                    continue

                asset_return = (
                    current_price
                    / previous_price
                ) - Decimal("1")

                weight = weights[
                    item["symbol"]
                ]

                portfolio_return += (
                    weight * asset_return
                )

                valid_weight += weight

            if valid_weight <= Decimal("0"):
                continue

            portfolio_return /= valid_weight

            previous_benchmark = benchmark_prices[
                previous_date
            ]

            current_benchmark = benchmark_prices[
                current_date
            ]

            if previous_benchmark <= Decimal("0"):
                continue

            benchmark_return = (
                current_benchmark
                / previous_benchmark
            ) - Decimal("1")

            portfolio_returns.append(
                portfolio_return
            )

            aligned_benchmark_returns.append(
                benchmark_return
            )

        # ---------------------------------------------------------
        # Validate observations
        # ---------------------------------------------------------

        observation_count = len(
            portfolio_returns
        )

        if observation_count < 2:

            return {
                **base_response,
                "beta": None,
                "observation_count": observation_count,
                "message": (
                    "Insufficient return observations"
                ),
            }

        # ---------------------------------------------------------
        # Beta
        # ---------------------------------------------------------

        benchmark_variance = _variance(
            aligned_benchmark_returns
        )

        if benchmark_variance <= Decimal("0"):

            return {
                **base_response,
                "beta": None,
                "observation_count": observation_count,
                "message": (
                    "Benchmark variance is zero"
                ),
            }

        covariance = _covariance(
            portfolio_returns,
            aligned_benchmark_returns,
        )

        beta = (
            covariance
            / benchmark_variance
        )

        return {
            **base_response,
            "beta": _percent(beta),
            "observation_count": observation_count,
            "portfolio_return_mean": _percent(
                _mean(portfolio_returns)
                * Decimal("100")
            ),
            "benchmark_return_mean": _percent(
                _mean(aligned_benchmark_returns)
                * Decimal("100")
            ),
        }


portfolio_beta_service = PortfolioBetaService()