class DriftAlertEngine:

    @staticmethod
    def generate(
        model_report,
    ):

        alerts = []

        # -------------------------
        # Feature Drift
        # -------------------------

        feature_drift = model_report.get(
            "feature_drift",
            {},
        )

        for feature, values in feature_drift.items():

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

        prediction = model_report.get(
            "prediction_drift",
            {},
        )

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
        # Model Drift
        # -------------------------

        model_drift = model_report.get(
            "model_drift",
            {},
        )

        if model_drift.get(
            "drift_detected",
            False,
        ):

            severity = model_drift.get(
                "severity",
                "HIGH",
            )

            if severity == "UNKNOWN":
                severity = "HIGH"

            alerts.append({

                "severity": severity,

                "type": "Model Drift",

                "message":
                    (
                        "Model performance has "
                        "degraded."
                    ),

            })

        # -------------------------
        # Target Drift
        # -------------------------

        target_drift = model_report.get(
            "target_drift",
            {},
        )

        if target_drift.get(
            "drift_detected",
            False,
        ):

            severity = target_drift.get(
                "severity",
                "HIGH",
            )

            if severity == "UNKNOWN":
                severity = "HIGH"

            alerts.append({

                "severity": severity,

                "type": "Target Drift",

                "message":
                    (
                        "Target distribution has "
                        "shifted."
                    ),

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
            alert["severity"] in {
                "HIGH",
                "CRITICAL",
            }
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