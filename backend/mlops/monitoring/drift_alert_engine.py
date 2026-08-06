class DriftAlertEngine:

    @staticmethod
    def generate(
        model_report,
    ):

        alerts = []

        # -------------------------
        # Feature Drift
        # -------------------------

        for feature, values in model_report[
            "feature_drift"
        ].items():

            if values.get(
                "drift_detected",
                False,
            ):

                alerts.append({

                    "severity": "HIGH",

                    "type": "Feature Drift",

                    "feature": feature,

                    "message":
                        f"{feature} distribution has drifted.",

                })

        # -------------------------
        # Prediction Drift
        # -------------------------

        prediction = model_report[
            "prediction_drift"
        ]

        if prediction.get(
            "drift_detected",
            False,
        ):

            alerts.append({

                "severity": "HIGH",

                "type": "Prediction Drift",

                "message":
                    "Prediction distribution has drifted.",

            })

        # -------------------------
        # Accuracy Check
        # -------------------------

        registry = model_report.get(
            "registry",
            {},
        )

        metrics = registry.get(
            "metrics",
            {},
        )

        accuracy = metrics.get(
            "directional_accuracy",
        )

        if (
            accuracy is not None
            and accuracy < 55
        ):

            alerts.append({

                "severity": "MEDIUM",

                "type": "Accuracy",

                "message":
                    (
                        "Directional accuracy "
                        "below acceptable threshold."
                    ),

            })

        # -------------------------
        # Retraining Recommendation
        # -------------------------

        if any(

            alert["severity"] == "HIGH"

            for alert in alerts

        ):

            alerts.append({

                "severity": "INFO",

                "type": "Recommendation",

                "message":
                    (
                        "Model retraining is "
                        "recommended."
                    ),

            })

        return alerts