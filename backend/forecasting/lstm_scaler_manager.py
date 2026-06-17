import pickle


class LSTMScalerManager:

    @staticmethod
    def save(
        scaler,
        path: str,
    ):
        with open(path, "wb") as f:
            pickle.dump(
                scaler,
                f
            )

    @staticmethod
    def load(
        path: str
    ):
        with open(path, "rb") as f:
            return pickle.load(
                f
            )