from database.session import (
    SessionLocal,
)

from services.monitoring_history_service import (
    MonitoringHistoryService,
)

from mlops.monitoring.model_performance_monitor import (
    ModelPerformanceMonitor,
)

from mlops.monitoring.retraining_recommendation_engine import (
    RetrainingRecommendationEngine,
)

import pandas as pd


def test():

    training = pd.DataFrame({

        "rsi": [45, 50, 55],

        "macd": [0.2, 0.3, 0.4],

    })

    production = pd.DataFrame({

        "rsi": [70, 72, 69],

        "macd": [0.2, 0.3, 0.4],

    })

    historical_predictions = [

        1.0,
        1.1,
        0.9,

    ]

    recent_predictions = [

        5.0,
        5.2,
        4.9,

    ]

    report = (
        ModelPerformanceMonitor.monitor(
            model_name="xgboost",
            symbol="RELIANCE",
            horizon="5d",
            training_features=training,
            production_features=production,
            historical_predictions=historical_predictions,
            recent_predictions=recent_predictions,

            # Phase 11 model-drift inputs
            historical_evaluations=[],
            recent_evaluations=[],

            # Phase 11 target-drift inputs
            historical_targets=[],
            recent_targets=[],
        )
    )

    recommendation = (
        RetrainingRecommendationEngine.recommend(
            report
        )
    )

    db = SessionLocal()

    try:

        result = (
            MonitoringHistoryService.save(
                db=db,
                report=report,
                recommendation=recommendation,
            )
        )

        print({

            "id": result.id,

            "model_name": result.model_name,

            "status": result.status,

            "priority": result.priority,

        })

        assert result.id is not None

        assert result.model_name == "xgboost"

    finally:

        db.close()


if __name__ == "__main__":
    test()