import pandas as pd

from risk.volatility_engine import VolatilityEngine


def test_historical_volatility():
    prices = pd.Series(
        [100, 101, 103, 102, 105, 107, 110]
    )

    volatility = VolatilityEngine.historical_volatility(prices)

    assert volatility > 0


def test_annualized_volatility():
    prices = pd.Series(
        [100, 101, 103, 102, 105, 107, 110]
    )

    volatility = VolatilityEngine.annualized_volatility(prices)

    assert volatility > 0


def test_volatility_classification():
    assert VolatilityEngine.classify_volatility(10) == "Low"
    assert VolatilityEngine.classify_volatility(20) == "Moderate"
    assert VolatilityEngine.classify_volatility(40) == "High"
    assert VolatilityEngine.classify_volatility(60) == "Very High"