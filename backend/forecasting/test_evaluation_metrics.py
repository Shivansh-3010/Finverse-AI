from types import SimpleNamespace

from forecasting.evaluation_metrics_engine import (
    EvaluationMetricsEngine,
)


def make_evaluation(
    predicted_return,
    actual_return,
    directional_correct=None,
):
    if directional_correct is None:
        directional_correct = float(
            (
                predicted_return >= 0
                and actual_return >= 0
            )
            or (
                predicted_return < 0
                and actual_return < 0
            )
        )

    return SimpleNamespace(
        predicted_return=float(predicted_return),
        actual_return=float(actual_return),
        absolute_error=abs(
            float(predicted_return)
            - float(actual_return)
        ),
        directional_correct=float(
            directional_correct
        ),
    )


def test_mae():
    evaluations = [
        make_evaluation(1.5, 1.0),
        make_evaluation(2.0, 2.0),
        make_evaluation(2.5, 3.0),
    ]

    result = EvaluationMetricsEngine.mae(
        evaluations
    )

    assert round(result, 6) == round(
        (0.5 + 0.0 + 0.5) / 3,
        6,
    )


def test_rmse():
    evaluations = [
        make_evaluation(1.5, 1.0),
        make_evaluation(2.0, 2.0),
        make_evaluation(2.5, 3.0),
    ]

    result = EvaluationMetricsEngine.rmse(
        evaluations
    )

    expected = (
        (
            0.5 ** 2
            + 0.0 ** 2
            + 0.5 ** 2
        )
        / 3
    ) ** 0.5

    assert round(result, 6) == round(
        expected,
        6,
    )


def test_mape_ignores_zero_and_near_zero():
    evaluations = [
        make_evaluation(1.0, 0.0),
        make_evaluation(1.0, 0.00001),
        make_evaluation(1.1, 1.0),
        make_evaluation(1.8, 2.0),
    ]

    result = EvaluationMetricsEngine.mape(
        evaluations
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
    evaluations = [
        make_evaluation(1.0, 0.0),
        make_evaluation(2.0, 0.00001),
    ]

    assert (
        EvaluationMetricsEngine.mape(
            evaluations
        )
        == 0.0
    )


def test_smape():
    evaluations = [
        make_evaluation(1.1, 1.0),
        make_evaluation(1.8, 2.0),
    ]

    result = EvaluationMetricsEngine.smape(
        evaluations
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
    evaluations = [
        make_evaluation(1.0, 2.0, 1.0),
        make_evaluation(-1.0, -2.0, 1.0),
        make_evaluation(1.0, -2.0, 0.0),
        make_evaluation(-1.0, 2.0, 0.0),
    ]

    result = (
        EvaluationMetricsEngine
        .directional_accuracy(
            evaluations
        )
    )

    assert result == 50.0


def test_empty_evaluations():
    assert (
        EvaluationMetricsEngine.mae([])
        == 0.0
    )

    assert (
        EvaluationMetricsEngine.rmse([])
        == 0.0
    )

    assert (
        EvaluationMetricsEngine.mape([])
        == 0.0
    )

    assert (
        EvaluationMetricsEngine.smape([])
        == 0.0
    )

    assert (
        EvaluationMetricsEngine
        .directional_accuracy([])
        == 0.0
    )

    assert (
        EvaluationMetricsEngine.hit_rate([])
        == 0.0
    )

    assert (
        EvaluationMetricsEngine.mean_bias([])
        == 0.0
    )

    assert (
        EvaluationMetricsEngine
        .max_absolute_error([])
        == 0.0
    )