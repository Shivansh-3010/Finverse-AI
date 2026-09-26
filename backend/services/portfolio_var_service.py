from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta, timezone
from math import sqrt
from statistics import mean
from uuid import UUID

from sqlalchemy.orm import Session

from repositories.ohlcv_repository import OHLCVRepository
from services.holding_service import holding_service


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioVaRService:
    """
    Calculates historical portfolio Value at Risk (VaR)
    and Expected Shortfall (CVaR).

    Metrics:
        - 95% historical VaR
        - 99% historical VaR
        - 95% Expected Shortfall
        - 99% Expected Shortfall
        - Worst historical return
        - Portfolio loss estimates
    """

    def __init__(self) -> None:
        self.ohlcv_repository = OHLCVRepository

    @staticmethod
    def _percentile(
        values: list[float],
        percentile: float,
    ) -> float | None:

        if not values:
            return None

        ordered = sorted(values)

        if len(ordered) == 1:
            return ordered[0]

        position = (
            (len(ordered) - 1)
            * percentile
        )

        lower = int(position)
        upper = min(
            lower + 1,
            len(ordered) - 1,
        )

        weight = position - lower

        return (
            ordered[lower]
            + (
                ordered[upper]
                - ordered[lower]
            )
            * weight
        )

    @staticmethod
    def _returns(
        values: list[float],
    ) -> list[float]:

        if len(values) < 2:
            return []

        returns = []

        for previous, current in zip(
            values,
            values[1:],
        ):
            if previous == 0:
                continue

            returns.append(
                (current / previous) - 1.0
            )

        return returns

    def _portfolio_returns(
        self,
        db: Session,
        portfolio_id: UUID,
        timeframe: str,
        lookback_days: int,
    ) -> list[float]:

        holdings = (
            holding_service.calculate_from_transactions(
                db,
                portfolio_id,
            )
        )

        if not holdings:
            return []

        end = datetime.now(timezone.utc)
        start = (
            end
            - timedelta(days=lookback_days)
        )

        prices_by_symbol = {}

        for holding in holdings:

            symbol = holding["symbol"]

            rows = (
                self.ohlcv_repository(db)
                .get_history_by_symbol_and_timeframe_between(
                    symbol,
                    timeframe,
                    start,
                    end,
                )
            )

            if rows:

                prices_by_symbol[symbol] = {
                    row.timestamp: float(row.close)
                    for row in rows
                    if row.close is not None
                }

        if not prices_by_symbol:
            return []

        common_dates = None

        for prices in prices_by_symbol.values():

            dates = set(prices.keys())

            if common_dates is None:
                common_dates = dates
            else:
                common_dates &= dates

        if not common_dates or len(common_dates) < 2:
            return []

        dates = sorted(common_dates)

        weights = {
            holding["symbol"]: float(
                holding["cost_basis"]
            )
            for holding in holdings
            if holding["symbol"]
            in prices_by_symbol
        }

        total_weight = sum(
            weights.values()
        )

        if total_weight <= 0:
            return []

        normalized_weights = {
            symbol: value / total_weight
            for symbol, value in weights.items()
        }

        portfolio_prices = []

        for date in dates:

            portfolio_value = 0.0

            for symbol, weight in (
                normalized_weights.items()
            ):
                portfolio_value += (
                    weight
                    * prices_by_symbol[
                        symbol
                    ][date]
                )

            portfolio_prices.append(
                portfolio_value
            )

        return self._returns(
            portfolio_prices
        )

    @staticmethod
    def _expected_shortfall(
        returns: list[float],
        percentile: float,
    ) -> float | None:

        if not returns:
            return None

        threshold = (
            PortfolioVaRService
            ._percentile(
                returns,
                percentile,
            )
        )

        if threshold is None:
            return None

        tail = [
            value
            for value in returns
            if value <= threshold
        ]

        if not tail:
            return threshold

        return mean(tail)

    def calculate(
        self,
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        returns = self._portfolio_returns(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
            lookback_days=lookback_days,
        )

        if len(returns) < 5:

            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "observation_count": len(
                    returns
                ),
                "var_95_pct": None,
                "var_99_pct": None,
                "var_95_value": None,
                "var_99_value": None,
                "expected_shortfall_95_pct": None,
                "expected_shortfall_99_pct": None,
                "expected_shortfall_95_value": None,
                "expected_shortfall_99_value": None,
                "worst_historical_return_pct": None,
                "risk_category": "Insufficient Data",
                "risk_flags": [
                    "Insufficient historical return data"
                ],
                "message": (
                    "At least 5 return observations "
                    "are required"
                ),
            }

        holdings = (
            holding_service.calculate_from_transactions(
                db,
                portfolio_id,
            )
        )

        total_market_value = sum(
            (
                Decimal(
                    str(
                        holding.get(
                            "market_value",
                            holding.get(
                                "cost_basis",
                                0,
                            ),
                        )
                    )
                )
                for holding in holdings
            ),
            Decimal("0"),
        )

        var_95_return = self._percentile(
            returns,
            0.05,
        )

        var_99_return = self._percentile(
            returns,
            0.01,
        )

        es_95_return = self._expected_shortfall(
            returns,
            0.05,
        )

        es_99_return = self._expected_shortfall(
            returns,
            0.01,
        )

        worst_return = min(returns)

        var_95_pct = (
            abs(var_95_return)
            if var_95_return is not None
            else None
        )

        var_99_pct = (
            abs(var_99_return)
            if var_99_return is not None
            else None
        )

        es_95_pct = (
            abs(es_95_return)
            if es_95_return is not None
            else None
        )

        es_99_pct = (
            abs(es_99_return)
            if es_99_return is not None
            else None
        )

        var_95_value = (
            total_market_value
            * Decimal(str(var_95_pct))
            if var_95_pct is not None
            else None
        )

        var_99_value = (
            total_market_value
            * Decimal(str(var_99_pct))
            if var_99_pct is not None
            else None
        )

        es_95_value = (
            total_market_value
            * Decimal(str(es_95_pct))
            if es_95_pct is not None
            else None
        )

        es_99_value = (
            total_market_value
            * Decimal(str(es_99_pct))
            if es_99_pct is not None
            else None
        )

        if var_99_pct is not None and var_99_pct >= 10:

            risk_category = "Severe Risk"

        elif var_99_pct is not None and var_99_pct >= 5:

            risk_category = "High Risk"

        elif var_99_pct is not None and var_99_pct >= 2:

            risk_category = "Moderate Risk"

        else:

            risk_category = "Low Risk"

        risk_flags = []

        if (
            var_95_pct is not None
            and var_95_pct >= 5
        ):
            risk_flags.append(
                "95% VaR indicates significant daily loss potential"
            )

        if (
            var_99_pct is not None
            and var_99_pct >= 10
        ):
            risk_flags.append(
                "99% VaR indicates severe tail risk"
            )

        if (
            es_99_pct is not None
            and es_99_pct > var_99_pct
        ):
            risk_flags.append(
                "Expected Shortfall exceeds 99% VaR"
            )

        if worst_return <= -0.10:
            risk_flags.append(
                "Portfolio has experienced a historical daily loss exceeding 10%"
            )

        if not risk_flags:
            risk_flags.append(
                "No major VaR risks detected"
            )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "observation_count": len(returns),
            "var_95_pct": _round(
                Decimal(str(var_95_pct * 100))
            )
            if var_95_pct is not None
            else None,
            "var_99_pct": _round(
                Decimal(str(var_99_pct * 100))
            )
            if var_99_pct is not None
            else None,
            "var_95_value": _round(
                var_95_value
            )
            if var_95_value is not None
            else None,
            "var_99_value": _round(
                var_99_value
            )
            if var_99_value is not None
            else None,
            "expected_shortfall_95_pct": _round(
                Decimal(str(es_95_pct * 100))
            )
            if es_95_pct is not None
            else None,
            "expected_shortfall_99_pct": _round(
                Decimal(str(es_99_pct * 100))
            )
            if es_99_pct is not None
            else None,
            "expected_shortfall_95_value": _round(
                es_95_value
            )
            if es_95_value is not None
            else None,
            "expected_shortfall_99_value": _round(
                es_99_value
            )
            if es_99_value is not None
            else None,
            "worst_historical_return_pct": _round(
                Decimal(str(worst_return * 100))
            ),
            "risk_category": risk_category,
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_var_service = PortfolioVaRService()