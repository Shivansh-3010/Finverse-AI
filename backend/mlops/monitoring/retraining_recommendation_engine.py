class RetrainingRecommendationEngine:

    @staticmethod
    def recommend(
        report,
    ):

        reasons = []

        recommend = False

        priority = "LOW"

        feature_drift = report.get(
            "feature_drift",
            {},
        )

        prediction_drift = report.get(
            "prediction_drift",
            {},
        )

        registry = report.get(
            "registry",
            {},
        )

        metrics = registry.get(
            "metrics",
            {},
        )

        # -----------------------------
        # Feature Drift
        # -----------------------------

        feature_drift_detected = any(

            feature.get(
                "drift_detected",
                False,
            )

            for feature in feature_drift.values()

        )

        if feature_drift_detected:

            reasons.append(
                "Feature Drift"
            )

            recommend = True

        # -----------------------------
        # Prediction Drift
        # -----------------------------

        if prediction_drift.get(
            "drift_detected",
            False,
        ):

            reasons.append(
                "Prediction Drift"
            )

            recommend = True

        # -----------------------------
        # Accuracy Check
        # -----------------------------

        directional_accuracy = metrics.get(
            "directional_accuracy",
        )

        if (

            directional_accuracy is not None

            and

            directional_accuracy < 55

        ):

            reasons.append(
                "Low Directional Accuracy"
            )

            recommend = True

        # -----------------------------
        # Priority
        # -----------------------------

        if len(reasons) == 0:

            priority = "LOW"

        elif len(reasons) == 1:

            priority = "MEDIUM"

        elif len(reasons) == 2:

            priority = "HIGH"

        else:

            priority = "CRITICAL"

        # -----------------------------
        # Result
        # -----------------------------

        return {

            "recommend": recommend,

            "priority": priority,

            "reasons": reasons,

            "recommended_action": (

                "Retrain model"

                if recommend

                else

                "No action required"

            ),

        }