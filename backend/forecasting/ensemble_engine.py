class EnsembleEngine:

    @staticmethod
    def combine(
        xgb_prediction_pct: float,
        prophet_forecast_price: float,
        lstm_prediction_pct: float,
        transformer_prediction_pct: float,
        current_price: float,
        confidence: float = 50.0,
    ):

        prophet_return_pct = (
            (
                prophet_forecast_price
                - current_price
            )
            / current_price
        ) * 100

        ensemble_return = (
            xgb_prediction_pct
            + prophet_return_pct
            + lstm_prediction_pct
            + transformer_prediction_pct
        ) / 4

        if ensemble_return > 1:
            direction = "bullish"

        elif ensemble_return < -1:
            direction = "bearish"

        else:
            direction = "neutral"

        return {
            "ensemble_return_pct":
                round(
                    ensemble_return,
                    4
                ),

            "direction":
                direction,

            "confidence":
                round(
                    confidence,
                    2
                ),

            "xgboost_return_pct":
                round(
                    xgb_prediction_pct,
                    4
                ),

            "prophet_return_pct":
                round(
                    prophet_return_pct,
                    4
                ),
                
            "lstm_return_pct":
                round(
                    lstm_prediction_pct,
                    4
                ),
                
            "transformer_return_pct":
                round(
                    transformer_prediction_pct,
                    4
                ),
        }