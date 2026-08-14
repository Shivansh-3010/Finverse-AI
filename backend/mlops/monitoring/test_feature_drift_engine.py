import numpy as np
import pandas as pd

from mlops.monitoring.feature_drift_engine import (
    FeatureDriftEngine,
)


def test_feature_drift_detected():

    training = pd.DataFrame({
        "rsi": [
            45,
            48,
            50,
            52,
            55,
        ],
        "macd": [
            0.2,
            0.3,
            0.4,
            0.5,
            0.4,
        ],
    })

    production = pd.DataFrame({
        "rsi": [
            62,
            65,
            66,
            64,
            67,
        ],
        "macd": [
            0.25,
            0.30,
            0.35,
            0.40,
            0.50,
        ],
    })

    result = FeatureDriftEngine.calculate(
        training,
        production,
    )

    assert "rsi" in result
    assert "macd" in result

    assert result["rsi"]["drift_detected"] is True
    assert result["rsi"]["ks_statistic"] > 0
    assert 0 <= result["rsi"]["p_value"] <= 1
    assert result["rsi"]["drift_score"] == result["rsi"]["ks_statistic"]


def test_feature_drift_not_detected():

    training = pd.DataFrame({
        "rsi": [
            45,
            48,
            50,
            52,
            55,
        ],
    })

    production = pd.DataFrame({
        "rsi": [
            45,
            48,
            50,
            52,
            55,
        ],
    })

    result = FeatureDriftEngine.calculate(
        training,
        production,
    )

    assert result["rsi"]["drift_detected"] is False
    assert result["rsi"]["ks_statistic"] == 0.0


def test_missing_columns_are_ignored():

    training = pd.DataFrame({
        "rsi": [45, 48, 50],
        "macd": [0.2, 0.3, 0.4],
    })

    production = pd.DataFrame({
        "rsi": [46, 49, 51],
    })

    result = FeatureDriftEngine.calculate(
        training,
        production,
    )

    assert "rsi" in result
    assert "macd" not in result


def test_empty_columns_are_ignored():

    training = pd.DataFrame({
        "rsi": [np.nan, np.nan],
    })

    production = pd.DataFrame({
        "rsi": [50, 51],
    })

    result = FeatureDriftEngine.calculate(
        training,
        production,
    )

    assert result == {}