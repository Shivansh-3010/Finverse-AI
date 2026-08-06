from models.monitoring_history import (
    MonitoringHistory,
)

from repositories.monitoring_history_repository import (
    MonitoringHistoryRepository,
)


class MonitoringHistoryService:

    @staticmethod
    def save(
        db,
        report,
        recommendation,
    ):

        metrics = report["registry"]["metrics"]

        feature_drift = any(

            x["drift_detected"]

            for x in report[
                "feature_drift"
            ].values()

        )

        prediction_drift = report[
            "prediction_drift"
        ]["drift_detected"]

        entity = MonitoringHistory(

            model_name=report["model"],

            symbol=report["symbol"],

            horizon=report["horizon"],

            status=report["status"],

            feature_drift=feature_drift,

            prediction_drift=prediction_drift,

            priority=recommendation[
                "priority"
            ],

            recommendation=recommendation[
                "recommended_action"
            ],

            mae=metrics["mae"],

            rmse=metrics["rmse"],

            mape=metrics["mape"],

            directional_accuracy=metrics[
                "directional_accuracy"
            ],

        )

        return (
            MonitoringHistoryRepository(
                db
            ).save(entity)
        )