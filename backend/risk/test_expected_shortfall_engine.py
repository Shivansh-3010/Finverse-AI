import pandas as pd

from risk.expected_shortfall_engine import ExpectedShortfallEngine


def test_expected_shortfall():
    prices = pd.Series(
        [100, 102, 101, 105, 103, 99, 95, 90]
    )

    es = ExpectedShortfallEngine.calculate_expected_shortfall(
        prices,
        confidence_level=0.95
    )

    assert es >= 0


def test_expected_shortfall_returns_float():
    prices = pd.Series(
        [100, 102, 101, 105, 103, 99, 95, 90]
    )

    es = ExpectedShortfallEngine.calculate_expected_shortfall(
        prices
    )

    assert isinstance(es, float)