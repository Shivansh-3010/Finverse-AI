from statistics import stdev


class ModelDriftEngine:

    @staticmethod
    def calculate(
        predictions,
    ) -> float:

        if len(predictions) < 2:
            return 0.0

        values = [
            p.prediction
            for p in predictions
        ]

        try:
            return round(
                stdev(values),
                4
            )

        except Exception:
            return 0.0