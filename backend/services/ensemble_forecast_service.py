from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from services.model_comparison_service import (
    ModelComparisonService,
)

from forecasting.ensemble_engine import (
    EnsembleEngine,
)


class EnsembleForecastService:

    @staticmethod
    def forecast(
        db,
        symbol: str,
        timeframe: str = "1d"
    ):

        comparison = (
            ModelComparisonService.compare(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
            )
        )

        latest_candle = (
            OHLCVRepository(db)
            .get_latest_candle(
                symbol=symbol,
                timeframe=timeframe,
            )
        )

        current_price = (
            latest_candle.close
        )

        return (
            EnsembleEngine.combine(
                xgb_prediction_pct=
                    comparison["xgboost"][
                        "predicted_return_pct"
                    ],

                prophet_forecast_price=
                    comparison["prophet"][
                        "forecast"
                    ],

                lstm_prediction_pct=
                    comparison["lstm"][
                        "predicted_return_pct"
                    ],
                    
                transformer_prediction_pct=
                    comparison["transformer"][
                        "predicted_return_pct"
                    ],

                current_price=
                    current_price,

                confidence=
                    comparison["xgboost"].get(
                        "confidence",
                        50.0
                    ),
            )
        )