from xgboost import XGBRegressor


class XGBoostEngine:

    @staticmethod
    def build_model():

        return XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.05,
            objective="reg:squarederror",
            random_state=42
        )