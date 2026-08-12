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

from forecasting.horizons import (
    HORIZON_DAYS,
)

from metrics.monitoring_metrics import (
    MonitoringMetrics,
)


class EvaluationEngine:

    @staticmethod
    def evaluate(
        db,
        symbol: str,
        timeframe: str = "1d",
    ):

        predictions = (
            PredictionRepository(db)
            .get_latest_predictions(
                symbol=symbol,
                timeframe=timeframe,
            )
        )

        if not predictions:
            return None

        ohlcv_repository = (
            OHLCVRepository(db)
        )

        saved = []

        for prediction in predictions:

            horizon_days = HORIZON_DAYS.get(
                prediction.horizon
            )

            if horizon_days is None:
                continue

            candles = (
                ohlcv_repository
                .get_candles_at_or_after(
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=prediction.timestamp,
                    limit=horizon_days + 1,
                )
            )

            if len(candles) < horizon_days + 1:
                continue

            reference_close = (
                candles[0].close
            )

            future_close = (
                candles[horizon_days].close
            )

            if reference_close == 0:
                continue

            actual_return = (
                (
                    future_close
                    - reference_close
                )
                /
                reference_close
            ) * 100

            evaluation = (
                PredictionEvaluationPersistenceService
                .save_evaluation(
                    symbol=symbol,
                    timeframe=timeframe,
                    prediction_timestamp=prediction.timestamp,
                    horizon=prediction.horizon,
                    model_name=prediction.model_name,
                    predicted_return=prediction.prediction,
                    actual_return=actual_return,
                )
            )

            saved.append(evaluation)

        if not saved:
            return None

        evaluations = (
            PredictionEvaluationRepository(db)
            .get_history(
                symbol=symbol,
                timeframe=timeframe,
                horizon=saved[0].horizon,
            )
        )

        MonitoringMetrics.update_prediction_metrics(
            mae=EvaluationMetricsEngine.mae(
                evaluations
            ),

            rmse=EvaluationMetricsEngine.rmse(
                evaluations
            ),

            mape=EvaluationMetricsEngine.mape(
                evaluations
            ),

            smape=EvaluationMetricsEngine.smape(
                evaluations
            ),

            directional_accuracy=
                EvaluationMetricsEngine.directional_accuracy(
                    evaluations
                ),

            hit_rate=EvaluationMetricsEngine.hit_rate(
                evaluations
            ),

            mean_bias=
                EvaluationMetricsEngine.mean_bias(
                    evaluations
                ),

            max_absolute_error=
                EvaluationMetricsEngine.max_absolute_error(
                    evaluations
                ),
        )

        return saved