import pandas as pd

from forecasting.backtest_metrics_engine import (
    BacktestMetricsEngine,
)


def test():

    equity = pd.Series(
        [
            100000,
            101000,
            99500,
            103000,
            106000,
            104000,
            108000,
            111000,
        ]
    )

    result = (
        BacktestMetricsEngine.summary(
            equity
        )
    )

    assert "total_return" in result
    assert "cagr" in result
    assert "volatility" in result
    assert "sharpe_ratio" in result
    assert "sortino_ratio" in result
    assert "win_rate" in result
    assert "profit_factor" in result
    assert "max_drawdown" in result

    print(result)


if __name__ == "__main__":
    test()