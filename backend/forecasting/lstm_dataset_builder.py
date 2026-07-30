import numpy as np
import pandas as pd


class LSTMDatasetBuilder:
    """
    Builds datasets for LSTM models.

    Supports two modes:

    1. Legacy mode
       prices -> sequences -> next value

    2. Production mode
       DatasetBuilder output
       -> feature sequences
       -> target (predicted_return_pct)
    """

    TARGET_COLUMN = "target"

    @staticmethod
    def build(
        prices=None,
        dataset: pd.DataFrame | None = None,
        sequence_length: int = 30,
        target_column: str = TARGET_COLUMN,
    ):
        """
        Backward-compatible dataset builder.

        Parameters
        ----------
        prices:
            Legacy list/array of values.

        dataset:
            Dataset produced by DatasetBuilder.build()

        Returns
        -------
        X, y
        """

        # ==========================================================
        # Legacy Mode
        # ==========================================================

        if prices is not None:

            prices = np.asarray(
                prices,
                dtype=np.float32,
            )

            if len(prices) <= sequence_length:
                raise ValueError(
                    "Not enough price values."
                )

            X = []
            y = []

            for i in range(
                len(prices) - sequence_length
            ):

                X.append(
                    prices[
                        i:i + sequence_length
                    ]
                )

                y.append(
                    prices[
                        i + sequence_length
                    ]
                )

            X = np.asarray(
                X,
                dtype=np.float32,
            ).reshape(
                -1,
                sequence_length,
                1,
            )

            y = np.asarray(
                y,
                dtype=np.float32,
            )

            return X, y

        # ==========================================================
        # Production Mode
        # ==========================================================

        if dataset is None:
            raise ValueError(
                "Either prices or dataset must be provided."
            )

        if dataset.empty:
            raise ValueError(
                "Dataset is empty."
            )

        if target_column not in dataset.columns:
            raise ValueError(
                f"Target column '{target_column}' not found."
            )

        dataset = dataset.copy()

        dataset = dataset.replace(
            [np.inf, -np.inf],
            np.nan,
        )

        dataset = (
            dataset
            .dropna()
            .reset_index(drop=True)
        )

        feature_columns = [
            c
            for c in dataset.columns
            if c not in [
                target_column,
                "timestamp",
            ]
        ]

        features = dataset[
            feature_columns
        ].to_numpy(
            dtype=np.float32
        )

        targets = dataset[
            target_column
        ].to_numpy(
            dtype=np.float32
        )

        X = []
        y = []

        for i in range(
            sequence_length,
            len(dataset),
        ):

            X.append(
                features[
                    i-sequence_length:i
                ]
            )

            y.append(
                targets[i]
            )

        return (
            np.asarray(
                X,
                dtype=np.float32,
            ),
            np.asarray(
                y,
                dtype=np.float32,
            ),
        )