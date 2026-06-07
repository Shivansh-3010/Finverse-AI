import pandas as pd


class OHLCVTransformer:

    @staticmethod
    def transform(
        df: pd.DataFrame,
        symbol: str
    ) -> pd.DataFrame:

        transformed_df = df.reset_index()

        transformed_df = transformed_df.rename(
            columns={
                "Date": "timestamp",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )

        transformed_df["symbol"] = symbol

        return transformed_df[
            [
                "symbol",
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        ]