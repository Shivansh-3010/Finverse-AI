from forecasting.prophet_engine import (
    ProphetEngine,
)


class ProphetForecastService:

    @staticmethod
    def forecast(
        prophet_df,
        periods: int = 5,
    ):

        model = (
            ProphetEngine.build_model()
        )

        model.fit(
            prophet_df
        )

        future = (
            model.make_future_dataframe(
                periods=periods,
            )
        )

        forecast = (
            model.predict(
                future,
            )
        )

        latest = forecast.iloc[-1]

        current_value = float(
            prophet_df.iloc[-1]["y"]
        )

        forecast_value = float(
            latest["yhat"]
        )

        lower_bound = float(
            latest["yhat_lower"]
        )

        upper_bound = float(
            latest["yhat_upper"]
        )

        predicted_return_pct = (
            (
                forecast_value
                - current_value
            )
            / current_value
        ) * 100

        interval_width = (
            upper_bound
            - lower_bound
        )

        confidence = max(
            0.0,
            min(
                100.0,
                100.0
                - (
                    interval_width
                    / current_value
                    * 100.0
                ),
            ),
        )

        if predicted_return_pct > 1:
            direction = "bullish"

        elif predicted_return_pct < -1:
            direction = "bearish"

        else:
            direction = "neutral"

        return {

            "model": "prophet",

            "current_price": round(
                current_value,
                2,
            ),

            "prediction": round(
                forecast_value,
                2,
            ),

            "predicted_return_pct": round(
                predicted_return_pct,
                4,
            ),

            "lower_bound": round(
                lower_bound,
                2,
            ),

            "upper_bound": round(
                upper_bound,
                2,
            ),

            "direction": direction,

            "confidence": round(
                confidence,
                2,
            ),
        }