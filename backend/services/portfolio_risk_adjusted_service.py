from __future__ import annotations

from decimal import Decimal
from math import sqrt
from statistics import mean
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from services.benchmark_data_service import benchmark_data_service
from services.holding_service import holding_service
from repositories.ohlcv_repository import OHLCVRepository


class PortfolioRiskAdjustedService:
    """
    Calculates portfolio risk-adjusted performance metrics.

    Metrics:
        - Sharpe ratio
        - Sortino ratio
        - Treynor ratio
        - Jensen's alpha
        - Tracking error
    """

    def __init__(self) -> None:
        self.ohlcv_repository = OHLCVRepository

    @staticmethod
    def _safe_float(value: Any) -> float | None:
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _returns(values: list[float]) -> list[float]:
        if len(values) < 2:
            return []

        return [
            (current / previous) - 1.0
            for previous, current in zip(values, values[1:])
            if previous not in (0.0, None)
        ]

    @staticmethod
    def _mean(values: list[float]) -> float:
        return mean(values) if values else 0.0

    @staticmethod
    def _std(values: list[float]) -> float:
        if len(values) < 2:
            return 0.0

        avg = mean(values)
        variance = sum((x - avg) ** 2 for x in values) / (len(values) - 1)
        return sqrt(variance)

    @staticmethod
    def _downside_deviation(
        returns: list[float],
        target: float = 0.0,
    ) -> float:
        downside = [min(0.0, r - target) for r in returns]

        if not downside:
            return 0.0

        return sqrt(sum(x * x for x in downside) / len(downside))

    @staticmethod
    def _percent(value: float | None) -> Decimal | None:
        if value is None:
            return None

        return Decimal(str(round(value * 100.0, 4)))

    @staticmethod
    def _ratio(value: float | None) -> Decimal | None:
        if value is None:
            return None

        return Decimal(str(round(value, 4)))

    def _portfolio_prices(
        self,
        db: Session,
        portfolio_id: UUID,
        timeframe: str,
        lookback_days: int,
    ) -> dict[str, list[Any]]:
        holdings = holding_service.calculate_from_transactions(
            db,
            portfolio_id,
        )

        result: dict[str, list[Any]] = {}

        from datetime import datetime, timedelta, timezone

        end = datetime.now(timezone.utc)
        start = end - timedelta(days=lookback_days)

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
                result[symbol] = rows

        return result

    def _build_portfolio_returns(
        self,
        db: Session,
        portfolio_id: UUID,
        timeframe: str,
        lookback_days: int,
    ) -> list[float]:
        holdings = holding_service.calculate_from_transactions(
            db,
            portfolio_id,
        )

        if not holdings:
            return []

        prices_by_symbol = self._portfolio_prices(
            db,
            portfolio_id,
            timeframe,
            lookback_days,
        )

        if not prices_by_symbol:
            return []

        series: dict[str, dict[Any, float]] = {}

        for symbol, rows in prices_by_symbol.items():
            series[symbol] = {
                row.timestamp: float(row.close)
                for row in rows
                if row.close is not None
            }

        common_dates = None

        for prices in series.values():
            dates = set(prices.keys())

            if common_dates is None:
                common_dates = dates
            else:
                common_dates &= dates

        if not common_dates or len(common_dates) < 2:
            return []

        dates = sorted(common_dates)

        weights = {
            h["symbol"]: float(h["cost_basis"])
            for h in holdings
            if h["symbol"] in series
        }

        total_weight = sum(weights.values())

        if total_weight <= 0:
            return []

        normalized_weights = {
            symbol: value / total_weight
            for symbol, value in weights.items()
        }

        portfolio_prices = []

        for date in dates:
            value = 0.0

            for symbol, weight in normalized_weights.items():
                value += weight * series[symbol][date]

            portfolio_prices.append(value)

        return self._returns(portfolio_prices)

    def _benchmark_returns(
        self,
        benchmark: str,
        lookback_days: int,
    ) -> list[float]:
        history = benchmark_data_service.get_history(
            benchmark,
            period=f"{lookback_days}d",
            interval="1d",
        )

        closes = [
            self._safe_float(row.get("close"))
            for row in history
        ]

        closes = [
            value
            for value in closes
            if value is not None
        ]

        return self._returns(closes)

    def calculate(
        self,
        db: Session,
        portfolio_id: UUID,
        benchmark: str = "NIFTY50",
        timeframe: str = "1d",
        lookback_days: int = 30,
        risk_free_rate: float = 0.0,
    ) -> dict[str, Any]:

        portfolio_returns = self._build_portfolio_returns(
            db,
            portfolio_id,
            timeframe,
            lookback_days,
        )

        benchmark_returns = self._benchmark_returns(
            benchmark,
            lookback_days,
        )

        observation_count = min(
            len(portfolio_returns),
            len(benchmark_returns),
        )

        if observation_count < 2:
            return {
                "portfolio_id": portfolio_id,
                "benchmark": benchmark,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "observation_count": observation_count,
                "sharpe_ratio": None,
                "sortino_ratio": None,
                "treynor_ratio": None,
                "alpha": None,
                "tracking_error": None,
                "message": "Insufficient return history",
            }

        portfolio_returns = portfolio_returns[-observation_count:]
        benchmark_returns = benchmark_returns[-observation_count:]

        portfolio_mean = self._mean(portfolio_returns)
        benchmark_mean = self._mean(benchmark_returns)

        excess_returns = [
            r - risk_free_rate
            for r in portfolio_returns
        ]

        volatility = self._std(excess_returns)

        sharpe = (
            portfolio_mean - risk_free_rate
        ) / volatility if volatility > 0 else None

        downside = self._downside_deviation(
            portfolio_returns,
            risk_free_rate,
        )

        sortino = (
            (portfolio_mean - risk_free_rate) / downside
            if downside > 0
            else None
        )

        covariance = sum(
            (p - portfolio_mean) * (b - benchmark_mean)
            for p, b in zip(
                portfolio_returns,
                benchmark_returns,
            )
        )

        benchmark_variance = sum(
            (b - benchmark_mean) ** 2
            for b in benchmark_returns
        )

        beta = (
            covariance / benchmark_variance
            if benchmark_variance > 0
            else None
        )

        treynor = (
            (portfolio_mean - risk_free_rate) / beta
            if beta not in (None, 0.0)
            else None
        )

        alpha = (
            portfolio_mean
            - (
                risk_free_rate
                + beta * (
                    benchmark_mean - risk_free_rate
                )
            )
            if beta is not None
            else None
        )

        active_returns = [
            p - b
            for p, b in zip(
                portfolio_returns,
                benchmark_returns,
            )
        ]

        tracking_error = self._std(active_returns)

        return {
            "portfolio_id": portfolio_id,
            "benchmark": benchmark,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "observation_count": observation_count,
            "sharpe_ratio": self._ratio(sharpe),
            "sortino_ratio": self._ratio(sortino),
            "treynor_ratio": self._ratio(treynor),
            "alpha": self._percent(alpha),
            "tracking_error": self._percent(tracking_error),
            "portfolio_return_mean": self._percent(portfolio_mean),
            "benchmark_return_mean": self._percent(benchmark_mean),
            "beta": self._ratio(beta),
            "message": None,
        }


portfolio_risk_adjusted_service = PortfolioRiskAdjustedService()