from xgboost import XGBRegressor


class XGBoostTrainingService:

    DEFAULT_PARAMS = {
        "objective": "reg:squarederror",
        "n_estimators": 300,
        "max_depth": 6,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "random_state": 42,
    }

    @staticmethod
    def train(
        X_train,
        y_train,
        **kwargs,
    ):

        params = (
            XGBoostTrainingService.DEFAULT_PARAMS.copy()
        )

        params.update(kwargs)

        model = XGBRegressor(
            **params
        )

        model.fit(
            X_train,
            y_train,
        )

        return model