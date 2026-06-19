import pandas as pd

from forecasting.feature_builder import (
    FeatureBuilder,
)

from forecasting.model_loader import (
    ModelLoader,
)

from repositories.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)

from forecasting.evaluation_metrics_engine import (
    EvaluationMetricsEngine,
)

from forecasting.confidence_engine import (
    ConfidenceEngine,
)

from services.prophet_forecast_service import (
    ProphetForecastService,
)

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

from services.lstm_prediction_service import (
    LSTMPredictionService,
)

from services.transformer_prediction_service import (
    TransformerPredictionService,
)


class ModelComparisonService:

    @staticmethod
    def compare(
        db,
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        features = (
            FeatureBuilder.build(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
            )
        )

        feature_names = (
            ModelLoader.load_features(
                horizon=horizon
            )
        )

        model = (
            ModelLoader.load_model(
                horizon=horizon
            )
        )

        X = pd.DataFrame(
            [features],
            columns=feature_names,
        )

        prediction = float(
            model.predict(X)[0]
        )

        evaluations = (
            PredictionEvaluationRepository(db)
            .get_history(
                symbol,
                timeframe
            )
        )

        if evaluations:

            confidence = (
                ConfidenceEngine.calculate(
                    mae=
                        EvaluationMetricsEngine.mae(
                            evaluations
                        ),

                    directional_accuracy=
                        EvaluationMetricsEngine.directional_accuracy(
                            evaluations
                        ),
                )
            )

        else:

            confidence = 50.0

        xgb_result = {
            "symbol": symbol,
            "timeframe": timeframe,
            "predicted_return_pct": round(
                prediction,
                4
            ),
            "direction":
                (
                    "bullish"
                    if prediction > 0
                    else "bearish"
                ),
            "confidence":
                round(
                    confidence,
                    2
                ),
        }

        records = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe(
                symbol=symbol,
                timeframe=timeframe,
            )
        )

        df = ohlcv_to_dataframe(
            records
        )

        prophet_df = df[
            [
                "timestamp",
                "close",
            ]
        ].copy()

        prophet_df.columns = [
            "ds",
            "y",
        ]

        prophet_df["ds"] = (
            prophet_df["ds"]
            .dt.tz_localize(None)
        )

        prophet_result = (
            ProphetForecastService.forecast(
                prophet_df=prophet_df,
                periods=5,
            )
        )
        
        lstm_result = (
            LSTMPredictionService.predict(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
            )
        )
        
        transformer_result = (
            TransformerPredictionService.predict(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
            )
        )

        return {
            "xgboost": xgb_result,
            "prophet": prophet_result,
            "lstm": lstm_result,
            "transformer": transformer_result,
        }