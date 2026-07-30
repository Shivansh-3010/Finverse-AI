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
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        comparison = (
            ModelComparisonService.compare(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
                horizon=horizon,
            )
        )

        return (
            EnsembleEngine.combine(
                xgb_prediction_pct=
                    comparison["xgboost"][
                        "predicted_return_pct"
                    ],

                prophet_prediction_pct=
                    comparison["prophet"][
                        "predicted_return_pct"
                    ],

                lstm_prediction_pct=
                    comparison["lstm"][
                        "predicted_return_pct"
                    ],
                    
                transformer_prediction_pct=
                    comparison["transformer"][
                        "predicted_return_pct"
                    ],

                confidence=
                    comparison["xgboost"].get(
                        "confidence",
                        50.0
                    ),
            )
        )