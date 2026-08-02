from forecasting.rolling_evaluation_engine import (
    RollingEvaluationEngine,
)


class DummyEvaluation:

    def __init__(
        self,
        actual,
        predicted,
    ):

        self.actual_return = actual
        self.predicted_return = predicted
        self.absolute_error = abs(
            predicted - actual
        )

        self.directional_correct = (
            (
                actual >= 0
                and predicted >= 0
            )
            or (
                actual < 0
                and predicted < 0
            )
        )


def test():

    evaluations = []

    for i in range(100):

        evaluations.append(
            DummyEvaluation(
                actual=1.0,
                predicted=0.9,
            )
        )

    result = (
        RollingEvaluationEngine.evaluate(
            evaluations
        )
    )

    assert 20 in result
    assert 50 in result
    assert 100 in result

    print(result)