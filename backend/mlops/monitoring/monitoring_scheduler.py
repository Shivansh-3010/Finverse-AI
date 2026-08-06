from database.session import SessionLocal

from services.monitoring_history_service import (
    MonitoringHistoryService,
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
        horizon: str,
        training_features,
        production_features,
        historical_predictions,
        recent_predictions,
    ):

        report = (
            ModelPerformanceMonitor.monitor(
                model_name=model_name,
                symbol=symbol,
                horizon=horizon,
                training_features=training_features,
                production_features=production_features,
                historical_predictions=historical_predictions,
                recent_predictions=recent_predictions,
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