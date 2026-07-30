from forecasting.prophet_engine import (
    ProphetEngine,
)


class ProphetForecastService:

    @staticmethod
    def forecast(
        prophet_df,
        periods: int = 5
    ):

        model = (
            ProphetEngine.build_model()
        )

        model.fit(
            prophet_df
        )

        future = (
            model.make_future_dataframe(
                periods=periods
            )
        )

        forecast = (
            model.predict(
                future
            )
        )

        latest = forecast.iloc[-1]

        current_value = float(
            prophet_df.iloc[-1]["y"]
        )

        forecast_value = float(
            latest["yhat"]
        )

        predicted_return_pct = (
            (
                forecast_value - current_value
            )
            / current_value
        ) * 100

        if predicted_return_pct > 1:
            direction = "bullish"

        elif predicted_return_pct < -1:
            direction = "bearish"

        else:
            direction = "neutral"

        return {
            "predicted_return_pct": round(
                predicted_return_pct,
                4,
            ),
            "forecast": forecast_value,
            "lower_bound": float(
                latest["yhat_lower"]
            ),
            "upper_bound": float(
                latest["yhat_upper"]
            ),
            "direction": direction,
            "confidence": 50.0,
        }