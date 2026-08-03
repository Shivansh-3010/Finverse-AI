class ExplainabilityEngine:

    HIGH_CONFIDENCE = 80.0
    MEDIUM_CONFIDENCE = 60.0

    @staticmethod
    def explain(
        comparison: dict,
        ensemble: dict,
    ):

        confidence = ensemble["confidence"]

        if confidence >= ExplainabilityEngine.HIGH_CONFIDENCE:
            confidence_label = "high"

        elif confidence >= ExplainabilityEngine.MEDIUM_CONFIDENCE:
            confidence_label = "moderate"

        else:
            confidence_label = "low"

        bullish_models = []
        bearish_models = []
        neutral_models = []

        for model_name, result in comparison.items():

            direction = result.get(
                "direction",
                "neutral",
            )

            if direction == "bullish":
                bullish_models.append(model_name.upper())

            elif direction == "bearish":
                bearish_models.append(model_name.upper())

            else:
                neutral_models.append(model_name.upper())

        reasons = []

        if bullish_models:
            reasons.append(
                f"Bullish: {', '.join(bullish_models)}"
            )

        if bearish_models:
            reasons.append(
                f"Bearish: {', '.join(bearish_models)}"
            )

        if neutral_models:
            reasons.append(
                f"Neutral: {', '.join(neutral_models)}"
            )

        return {

            "forecast": (
                "BUY"
                if ensemble["direction"] == "bullish"
                else (
                    "SELL"
                    if ensemble["direction"] == "bearish"
                    else "HOLD"
                )
            ),

            "direction":
                ensemble["direction"],

            "confidence":
                confidence,

            "confidence_label":
                confidence_label,

            "agreement_score":
                ensemble["agreement_score"],

            "models_used":
                ensemble["models_used"],

            "reason":
                "; ".join(reasons),

            "model_predictions":
                ensemble["model_predictions"],
        }