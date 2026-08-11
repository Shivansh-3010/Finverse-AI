import numpy as np

from forecasting.metrics_engine import (
    MetricsEngine,
)


def test_mae():

    result = MetricsEngine.mae(
        [1.0, 2.0, 3.0],
        [1.5, 2.0, 2.5],
    )

    assert result == 1 / 3


def test_rmse():

    result = MetricsEngine.rmse(
        [1.0, 2.0, 3.0],
        [1.5, 2.0, 2.5],
    )

    assert round(result, 6) == round(
        np.sqrt(
            (
                0.25
                + 0.0
                + 0.25
            )
            / 3
        ),
        6,
    )


def test_mape_ignores_zero_and_near_zero():

    result = MetricsEngine.mape(
        [
            0.0,
            0.00001,
            1.0,
            2.0,
        ],
        [
            1.0,
            1.0,
            1.1,
            1.8,
        ],
    )

    expected = (
        (
            abs(1.0 - 1.1) / 1.0
            +
            abs(2.0 - 1.8) / 2.0
        )
        / 2
    ) * 100

    assert round(result, 6) == round(
        expected,
        6,
    )


def test_mape_all_zero_returns_zero():

    result = MetricsEngine.mape(
        [0.0, 0.0, 0.00001],
        [1.0, 2.0, 3.0],
    )

    assert result == 0.0


def test_smape():

    result = MetricsEngine.smape(
        [1.0, 2.0],
        [1.1, 1.8],
    )

    expected = (
        (
            2 * abs(1.1 - 1.0)
            / (abs(1.0) + abs(1.1))
            +
            2 * abs(1.8 - 2.0)
            / (abs(2.0) + abs(1.8))
        )
        / 2
    ) * 100

    assert round(result, 6) == round(
        expected,
        6,
    )


def test_directional_accuracy():

    result = (
        MetricsEngine.directional_accuracy(
            [
                2.0,
                -1.0,
                3.0,
                -2.0,
            ],
            [
                1.0,
                -2.0,
                -1.0,
                -3.0,
            ],
        )
    )

    assert result == 75.0