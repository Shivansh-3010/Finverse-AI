from prophet import Prophet


class ProphetEngine:

    @staticmethod
    def build_model():

        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True,
        )

        regressors = [
            "close",
            "volume",
            "rsi",
            "macd",
            "adx",
            "atr",
            "obv",
            "vwap",
            "mfi",
            "candlestick_score",
            "risk_score",
            "signal_value",
            "avg_news_score",
        ]

        for feature in regressors:
            model.add_regressor(feature)

        return model