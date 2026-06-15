import pandas as pd

from risk.drawdown_engine import DrawdownEngine


def test_max_drawdown():
    prices = pd.Series(
        [100, 110, 120, 90, 95, 80]
    )

    drawdown = DrawdownEngine.max_drawdown(prices)

    assert drawdown < 0


def test_drawdown_classification():
    assert DrawdownEngine.classify_drawdown(-5) == "Low"
    assert DrawdownEngine.classify_drawdown(-15) == "Moderate"
    assert DrawdownEngine.classify_drawdown(-25) == "High"
    assert DrawdownEngine.classify_drawdown(-40) == "Very High"