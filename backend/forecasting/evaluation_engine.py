from repositories.prediction_repository import (
    PredictionRepository,
)

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from services.prediction_evaluation_persistence_service import (
    PredictionEvaluationPersistenceService,
)
from repositories.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)

from forecasting.evaluation_metrics_engine import (
    EvaluationMetricsEngine,
)

from metrics.monitoring_metrics import (
    MonitoringMetrics,
)


class EvaluationEngine:

    @staticmethod
    def evaluate(
        db,
        symbol: str,
        timeframe: str = "1d"
    ):

        prediction = (
            PredictionRepository(db)
            .get_latest(
                symbol,
                timeframe
            )
        )

        if not prediction:
            return None

        candles = (
            OHLCVRepository(db)
            .get_latest_by_symbol_and_timeframe(
                symbol=symbol,
                timeframe=timeframe,
                limit=2
            )
        )

        if len(candles) < 2:
            return None

        previous_close = (
            candles[1].close
        )

        latest_close = (
            candles[0].close
        )

        actual_return = (
            (
                latest_close
                - previous_close
            )
            /
            previous_close
        ) * 100

        saved = (
            PredictionEvaluationPersistenceService
            .save_evaluation(
                symbol=symbol,
                timeframe=timeframe,
                model_name=
                    prediction.model_name,
                predicted_return=
                    prediction.prediction,
                actual_return=
                    actual_return,
            )
        )

        evaluations = (
            PredictionEvaluationRepository(db)
            .get_history(
                symbol,
                timeframe
            )
        )

        MonitoringMetrics.update_prediction_metrics(
            mae=
                EvaluationMetricsEngine.mae(
                    evaluations
                ),

            rmse=
                EvaluationMetricsEngine.rmse(
                    evaluations
                ),

            mape=
                EvaluationMetricsEngine.mape(
                    evaluations
                ),

            directional_accuracy=
                EvaluationMetricsEngine.directional_accuracy(
                    evaluations
                ),
        )

        return saved