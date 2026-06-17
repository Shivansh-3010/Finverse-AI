import numpy as np


class LSTMDatasetBuilder:

    @staticmethod
    def build(
        prices,
        sequence_length: int = 30
    ):

        X = []
        y = []

        for i in range(
            len(prices)
            - sequence_length
        ):

            X.append(
                prices[
                    i:
                    i + sequence_length
                ]
            )

            y.append(
                prices[
                    i + sequence_length
                ]
            )

        X = np.array(X)
        y = np.array(y)

        X = X.reshape(
            (
                X.shape[0],
                X.shape[1],
                1
            )
        )

        return X, y