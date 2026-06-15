import pandas as pd

from risk.var_engine import ValueAtRiskEngine


def test_var_calculation():
    prices = pd.Series(
        [100, 102, 101, 105, 104, 108, 110]
    )

    var = ValueAtRiskEngine.calculate_var(
        prices,
        confidence_level=0.95
    )

    assert var >= 0


def test_var_higher_confidence():
    prices = pd.Series(
        [100, 102, 101, 105, 104, 108, 110]
    )

    var_95 = ValueAtRiskEngine.calculate_var(
        prices,
        confidence_level=0.95
    )

    var_99 = ValueAtRiskEngine.calculate_var(
        prices,
        confidence_level=0.99
    )

    assert var_99 >= var_95