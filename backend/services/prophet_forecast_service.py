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

        return {
            "forecast": float(
                latest["yhat"]
            ),
            "lower_bound": float(
                latest["yhat_lower"]
            ),
            "upper_bound": float(
                latest["yhat_upper"]
            ),
        }