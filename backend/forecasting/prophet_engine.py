from prophet import Prophet


class ProphetEngine:

    @staticmethod
    def build_model():

        return Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True,
        )