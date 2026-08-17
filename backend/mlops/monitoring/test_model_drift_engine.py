from types import SimpleNamespace

from mlops.monitoring.model_drift_engine import (
    ModelDriftEngine,
)


def make_evaluations(
    predicted,
    actual,
    count=10,
):

    evaluations = []

    for _ in range(count):

        evaluations.append(
            SimpleNamespace(
                predicted_return=predicted,
                actual_return=actual,
                absolute_error=abs(
                    predicted - actual
                ),
                directional_correct=float(
                    (
                        predicted >= 0
                        and actual >= 0
                    )
                    or (
                        predicted < 0
                        and actual < 0
                    )
                ),
            )
        )

    return evaluations


def test_model_drift_detected():

    historical = (
        make_evaluations(
            predicted=1.0,
            actual=1.0,
        )
    )

    recent = (
        make_evaluations(
            predicted=5.0,
            actual=1.0,
        )
    )

    result = ModelDriftEngine.calculate(
        historical,
        recent,
    )

    assert (
        result["status"]
        == "evaluated"
    )

    assert (
        result["drift_detected"]
        is True
    )

    assert (
        result["drift_score"]
        > 0
    )

    assert (
        result["metrics"]["mae"]["degraded"]
        is True
    )

    assert (
        result["metrics"]["rmse"]["degraded"]
        is True
    )


def test_model_drift_not_detected():

    historical = (
        make_evaluations(
            predicted=1.0,
            actual=1.0,
        )
    )

    recent = (
        make_evaluations(
            predicted=1.0,
            actual=1.0,
        )
    )

    result = ModelDriftEngine.calculate(
        historical,
        recent,
    )

    assert (
        result["status"]
        == "evaluated"
    )

    assert (
        result["drift_detected"]
        is False
    )

    assert (
        result["drift_score"]
        == 0.0
    )


def test_insufficient_data():

    historical = (
        make_evaluations(
            predicted=1.0,
            actual=1.0,
            count=5,
        )
    )

    recent = (
        make_evaluations(
            predicted=5.0,
            actual=1.0,
            count=5,
        )
    )

    result = ModelDriftEngine.calculate(
        historical,
        recent,
    )

    assert (
        result["status"]
        == "insufficient_data"
    )

    assert (
        result["drift_detected"]
        is False
    )

    assert (
        result["metrics"]
        == {}
    )


def test_accuracy_degradation_is_detected():

    historical = []

    recent = []

    for _ in range(10):

        historical.append(
            SimpleNamespace(
                predicted_return=1.0,
                actual_return=1.0,
                absolute_error=0.0,
                directional_correct=1.0,
            )
        )

        recent.append(
            SimpleNamespace(
                predicted_return=1.0,
                actual_return=-1.0,
                absolute_error=2.0,
                directional_correct=0.0,
            )
        )

    result = ModelDriftEngine.calculate(
        historical,
        recent,
    )

    assert (
        result["metrics"]
        ["directional_accuracy"]
        ["degraded"]
        is True
    )


if __name__ == "__main__":
    test_model_drift_detected()