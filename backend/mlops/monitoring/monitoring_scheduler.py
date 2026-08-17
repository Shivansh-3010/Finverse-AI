from database.session import SessionLocal

from services.monitoring_history_service import (
    MonitoringHistoryService,
)

from services.monitoring_data_service import (
    MonitoringDataService,
)

from mlops.monitoring.model_performance_monitor import (
    ModelPerformanceMonitor,
)

from mlops.monitoring.drift_alert_engine import (
    DriftAlertEngine,
)

from mlops.monitoring.retraining_recommendation_engine import (
    RetrainingRecommendationEngine,
)


class MonitoringScheduler:

    @staticmethod
    def run(
        model_name: str,
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        data = (
            MonitoringDataService
            .get_model_data(
                model_name=model_name,
                symbol=symbol,
                timeframe=timeframe,
                horizon=horizon,
            )
        )

        report = (
            ModelPerformanceMonitor.monitor(
                model_name=model_name,
                symbol=symbol,
                horizon=horizon,
                training_features=data[
                    "training_features"
                ],
                production_features=data[
                    "production_features"
                ],
                historical_predictions=data[
                    "historical_predictions"
                ],
                recent_predictions=data[
                    "recent_predictions"
                ],
                historical_evaluations=data[
                    "historical_evaluations"
                ],

                recent_evaluations=data[
                    "recent_evaluations"
                ],

                historical_targets=data[
                    "historical_targets"
                ],

                recent_targets=data[
                    "recent_targets"
                ],
            )
        )

        alerts = (
            DriftAlertEngine.generate(
                report
            )
        )

        recommendation = (
            RetrainingRecommendationEngine.recommend(
                report
            )
        )

        db = SessionLocal()

        try:

            MonitoringHistoryService.save(
                db=db,
                report=report,
                recommendation=recommendation,
            )

        finally:

            db.close()

        return {

            "report": report,

            "alerts": alerts,

            "recommendation": recommendation,

            "completed": True,

        }