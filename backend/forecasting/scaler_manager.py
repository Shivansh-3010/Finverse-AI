import joblib


class ScalerManager:

    @staticmethod
    def save(
        scaler,
        path: str,
    ):

        joblib.dump(
            scaler,
            path,
        )

    @staticmethod
    def load(
        path: str,
    ):

        return joblib.load(
            path,
        )