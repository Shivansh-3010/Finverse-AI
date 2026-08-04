import math

import numpy as np
import pandas as pd

from risk.drawdown_engine import (
    DrawdownEngine,
)


class BacktestMetricsEngine:

    RISK_FREE_RATE = 0.05
    
    EPSILON = 1e-8

    @staticmethod
    def total_return(
        equity_curve: pd.Series,
    ) -> float:

        if len(equity_curve) < 2:
            return 0.0

        return (
            (
                equity_curve.iloc[-1]
                / equity_curve.iloc[0]
            )
            - 1
        ) * 100

    @staticmethod
    def cagr(
        equity_curve: pd.Series,
        periods_per_year: int = 252,
    ) -> float:

        if len(equity_curve) < 2:
            return 0.0

        years = (
            len(equity_curve)
            / periods_per_year
        )

        if years <= 0:
            return 0.0

        return (
            (
                equity_curve.iloc[-1]
                / equity_curve.iloc[0]
            )
            ** (1 / years)
            - 1
        ) * 100

    @staticmethod
    def volatility(
        returns: pd.Series,
        periods_per_year: int = 252,
    ) -> float:

        if returns.empty:
            return 0.0

        return float(
            returns.std()
            * math.sqrt(periods_per_year)
            * 100
        )

    @staticmethod
    def sharpe_ratio(
        returns: pd.Series,
        periods_per_year: int = 252,
    ) -> float:

        if returns.empty:
            return 0.0

        excess_returns = (
            returns
            - (
                BacktestMetricsEngine.RISK_FREE_RATE
                / periods_per_year
            )
        )

        std = float(
            excess_returns.std()
        )

        if (
            math.isnan(std)
            or abs(std)
            < BacktestMetricsEngine.EPSILON
        ):
            return 0.0

        return float(
            (
                excess_returns.mean()
                / std
            )
            * math.sqrt(periods_per_year)
        )

    @staticmethod
    def sortino_ratio(
        returns: pd.Series,
        periods_per_year: int = 252,
    ) -> float:

        if returns.empty:
            return 0.0

        downside = returns[
            returns < 0
        ]

        if downside.empty:
            return 0.0

        downside_std = float(
            downside.std()
        )

        if (
            math.isnan(downside_std)
            or abs(downside_std)
            < BacktestMetricsEngine.EPSILON
        ):
            return 0.0

        excess_returns = (
            returns
            - (
                BacktestMetricsEngine.RISK_FREE_RATE
                / periods_per_year
            )
        )

        return float(
            (
                excess_returns.mean()
                / downside_std
            )
            * math.sqrt(periods_per_year)
        )

    @staticmethod
    def win_rate(
        returns: pd.Series,
    ) -> float:

        if returns.empty:
            return 0.0

        return float(
            (
                (returns > 0).sum()
                / len(returns)
            )
            * 100
        )

    @staticmethod
    def profit_factor(
        returns: pd.Series,
    ) -> float:

        gains = float(
            returns[
                returns > 0
            ].sum()
        )

        losses = abs(
            float(
                returns[
                    returns < 0
                ].sum()
            )
        )

        if losses < BacktestMetricsEngine.EPSILON:
            return 0.0

        return gains / losses

    @staticmethod
    def max_drawdown(
        equity_curve: pd.Series,
    ) -> float:

        return (
            DrawdownEngine.max_drawdown(
                equity_curve
            )
        )

    @staticmethod
    def summary(
        equity_curve: pd.Series,
    ):

        returns = (
            equity_curve
            .pct_change()
            .dropna()
        )

        return {

            "total_return": round(
                BacktestMetricsEngine.total_return(
                    equity_curve
                ),
                2,
            ),

            "cagr": round(
                BacktestMetricsEngine.cagr(
                    equity_curve
                ),
                2,
            ),

            "volatility": round(
                BacktestMetricsEngine.volatility(
                    returns
                ),
                2,
            ),

            "sharpe_ratio": round(
                BacktestMetricsEngine.sharpe_ratio(
                    returns
                ),
                4,
            ),

            "sortino_ratio": round(
                BacktestMetricsEngine.sortino_ratio(
                    returns
                ),
                4,
            ),

            "win_rate": round(
                BacktestMetricsEngine.win_rate(
                    returns
                ),
                2,
            ),

            "profit_factor": round(
                BacktestMetricsEngine.profit_factor(
                    returns
                ),
                4,
            ),

            "max_drawdown": round(
                BacktestMetricsEngine.max_drawdown(
                    equity_curve
                ),
                2,
            ),
        }