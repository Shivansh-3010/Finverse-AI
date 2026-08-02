class AdaptiveWeightEngine:

    MIN_WEIGHT = 0.05

    @staticmethod
    def calculate(
        leaderboard,
    ):

        if not leaderboard:
            return {}

        scores = {}

        for model in leaderboard:

            score = (
                model["directional_accuracy"] / 100.0
            ) / max(
                model["mae"],
                0.0001,
            )

            scores[
                model["model"]
            ] = score

        total_score = sum(
            scores.values()
        )

        weights = {}

        if total_score == 0:

            equal = (
                1.0
                / len(scores)
            )

            for model in scores:

                weights[model] = equal

            return weights

        for model, score in scores.items():

            weight = score / total_score

            weights[model] = max(
                weight,
                AdaptiveWeightEngine.MIN_WEIGHT,
            )

        normalization = sum(
            weights.values()
        )

        for model in weights:

            weights[model] /= normalization

        return weights