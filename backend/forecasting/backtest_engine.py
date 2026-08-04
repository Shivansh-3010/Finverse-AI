import pandas as pd

from forecasting.backtest_metrics_engine import (
    BacktestMetricsEngine,
)


class BacktestEngine:

    INITIAL_CAPITAL = 100000.0

    TRANSACTION_COST = 0.001

    @staticmethod
    def run(
        prediction_history,
    ):

        capital = (
            BacktestEngine.INITIAL_CAPITAL
        )

        equity_curve = [capital]

        trades = []

        for prediction in prediction_history:

            predicted_return = (
                prediction.predicted_return
            )
            actual_return = (
                prediction.actual_return
            )

            if predicted_return > 0:

                pnl = (
                    capital
                    * actual_return
                    / 100.0
                )

            else:

                pnl = (
                    -capital
                    * actual_return
                    / 100.0
                )

            cost = (
                capital
                * BacktestEngine.TRANSACTION_COST
            )

            pnl -= cost

            capital += pnl

            equity_curve.append(
                capital
            )

            trades.append(
                {
                    "timestamp":
                        prediction.timestamp,

                    "predicted_return":
                        predicted_return,

                    "actual_return":
                        actual_return,

                    "pnl":
                        round(
                            pnl,
                            2,
                        ),

                    "capital":
                        round(
                            capital,
                            2,
                        ),
                }
            )

        equity_curve = pd.Series(
            equity_curve
        )

        metrics = (
            BacktestMetricsEngine.summary(
                equity_curve
            )
        )

        return {

            "initial_capital":
                BacktestEngine.INITIAL_CAPITAL,

            "final_capital":
                round(
                    capital,
                    2,
                ),

            "equity_curve":
                equity_curve.tolist(),

            "trade_count":
                len(trades),

            "metrics":
                metrics,

            "trades":
                trades,
        }