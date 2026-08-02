import math


class EvaluationMetricsEngine:

    @staticmethod
    def mae(evaluations):

        if not evaluations:
            return 0.0

        return (
            sum(
                e.absolute_error
                for e in evaluations
            )
            / len(evaluations)
        )

    @staticmethod
    def rmse(evaluations):

        if not evaluations:
            return 0.0

        mse = (
            sum(
                (
                    e.predicted_return
                    - e.actual_return
                ) ** 2
                for e in evaluations
            )
            / len(evaluations)
        )

        return math.sqrt(mse)

    @staticmethod
    def directional_accuracy(evaluations):

        if not evaluations:
            return 0.0

        return (
            sum(
                e.directional_correct
                for e in evaluations
            )
            / len(evaluations)
        ) * 100

    @staticmethod
    def mape(evaluations):

        if not evaluations:
            return 0.0

        valid = [
            e
            for e in evaluations
            if e.actual_return != 0
        ]

        if not valid:
            return 0.0

        return (
            sum(
                abs(
                    (
                        e.actual_return
                        - e.predicted_return
                    )
                    / abs(e.actual_return)
                )
                for e in valid
            )
            / len(valid)
        ) * 100

    @staticmethod
    def smape(evaluations):

        if not evaluations:
            return 0.0

        valid = [
            e
            for e in evaluations
            if (
                abs(e.actual_return)
                + abs(e.predicted_return)
            ) > 0
        ]

        if not valid:
            return 0.0

        return (
            sum(
                (
                    2
                    * abs(
                        e.predicted_return
                        - e.actual_return
                    )
                )
                / (
                    abs(e.actual_return)
                    + abs(e.predicted_return)
                )
                for e in valid
            )
            / len(valid)
        ) * 100

    @staticmethod
    def hit_rate(evaluations):

        if not evaluations:
            return 0.0

        hits = sum(
            abs(e.predicted_return)
            <= abs(e.actual_return)
            for e in evaluations
        )

        return (
            hits
            / len(evaluations)
        ) * 100

    @staticmethod
    def mean_bias(evaluations):

        if not evaluations:
            return 0.0

        return (
            sum(
                e.predicted_return
                - e.actual_return
                for e in evaluations
            )
            / len(evaluations)
        )

    @staticmethod
    def max_absolute_error(evaluations):

        if not evaluations:
            return 0.0

        return max(
            e.absolute_error
            for e in evaluations
        )