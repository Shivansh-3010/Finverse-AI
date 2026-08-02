import statistics


class EnsembleEngine:

    DEFAULT_WEIGHTS = {
        "xgboost": 0.35,
        "lstm": 0.30,
        "transformer": 0.25,
        "prophet": 0.10,
    }

    BULLISH_THRESHOLD = 1.0
    BEARISH_THRESHOLD = -1.0

    AGREEMENT_MULTIPLIER = 20.0

    AGREEMENT_WEIGHT = 0.40
    MODEL_CONFIDENCE_WEIGHT = 0.60

    @staticmethod
    def combine(
        predictions: dict,
        comparison: dict,
        weights: dict | None = None,
    ):

        if weights is None:
            weights = (
                EnsembleEngine.DEFAULT_WEIGHTS
            )

        available_models = [
            model
            for model in predictions
            if model in weights
        ]

        if len(available_models) < 2:
            raise ValueError(
                "At least two predictions are required."
            )

        total_weight = sum(
            weights[model]
            for model in available_models
        )

        weighted_prediction = (
            sum(
                predictions[model]
                * weights[model]
                for model in available_models
            )
            / total_weight
        )

        prediction_values = [
            predictions[model]
            for model in available_models
        ]

        dispersion = (
            statistics.pstdev(
                prediction_values,
            )
            if len(prediction_values) > 1
            else 0.0
        )

        agreement_score = max(
            0.0,
            100.0
            - dispersion
            * EnsembleEngine.AGREEMENT_MULTIPLIER,
        )

        confidence_values = [
            comparison[model].get(
                "confidence",
                50.0,
            )
            for model in available_models
        ]

        model_confidence = (
            sum(confidence_values)
            / len(confidence_values)
        )

        confidence = (
            agreement_score
            * EnsembleEngine.AGREEMENT_WEIGHT
            + model_confidence
            * EnsembleEngine.MODEL_CONFIDENCE_WEIGHT
        )

        if (
            weighted_prediction
            > EnsembleEngine.BULLISH_THRESHOLD
        ):
            direction = "bullish"

        elif (
            weighted_prediction
            < EnsembleEngine.BEARISH_THRESHOLD
        ):
            direction = "bearish"

        else:
            direction = "neutral"

        explanation = [
            (
                f"{model.upper()}: "
                f"{predictions[model]:.4f}% "
                f"(weight={weights[model]:.3f})"
            )
            for model in available_models
        ]

        return {
            "ensemble_return_pct": round(
                weighted_prediction,
                4,
            ),

            "direction": direction,

            "confidence": round(
                confidence,
                2,
            ),

            "agreement_score": round(
                agreement_score,
                2,
            ),

            "weights": {
                model: round(
                    weights[model],
                    4,
                )
                for model in available_models
            },

            "models_used": available_models,

            "model_predictions": {
                model: round(
                    predictions[model],
                    4,
                )
                for model in available_models
            },

            "explanation": explanation,
        }