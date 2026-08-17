from mlops.monitoring.target_drift_engine import (
    TargetDriftEngine,
)


def test_target_drift_detected():

    historical = [
        -0.8,
        -0.2,
        0.1,
        0.4,
        0.7,
        0.9,
    ]

    recent = [
        4.8,
        5.1,
        5.0,
        4.9,
        5.2,
        5.4,
    ]

    result = (
        TargetDriftEngine.calculate(
            historical,
            recent,
        )
    )

    assert (
        result["drift_detected"]
        is True
    )

    assert (
        result["ks_statistic"] > 0
    )

    assert (
        0 <= result["p_value"] <= 1
    )

    assert (
        result["drift_score"]
        == result["ks_statistic"]
    )


def test_target_drift_not_detected():

    historical = [
        -0.8,
        -0.2,
        0.1,
        0.4,
        0.7,
        0.9,
    ]

    recent = [
        -0.8,
        -0.2,
        0.1,
        0.4,
        0.7,
        0.9,
    ]

    result = (
        TargetDriftEngine.calculate(
            historical,
            recent,
        )
    )

    assert (
        result["drift_detected"]
        is False
    )

    assert (
        result["ks_statistic"]
        == 0.0
    )


def test_empty_targets():

    result = (
        TargetDriftEngine.calculate(
            [],
            [1.0, 2.0],
        )
    )

    assert result == {}


def test_non_finite_targets_are_ignored():

    historical = [
        0.8,
        1.0,
        float("nan"),
        float("inf"),
    ]

    recent = [
        0.8,
        1.0,
        1.1,
    ]

    result = (
        TargetDriftEngine.calculate(
            historical,
            recent,
        )
    )

    assert result

    assert (
        0 <= result["p_value"] <= 1
    )


if __name__ == "__main__":
    test_target_drift_detected()