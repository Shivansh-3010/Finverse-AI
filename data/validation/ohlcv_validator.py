import pandas as pd


class OHLCVValidator:

    REQUIRED_COLUMNS = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    @staticmethod
    def validate_empty(df: pd.DataFrame) -> bool:
        return not df.empty

    @staticmethod
    def validate_required_columns(df: pd.DataFrame) -> bool:
        return all(
            col in df.columns
            for col in OHLCVValidator.REQUIRED_COLUMNS
        )

    @staticmethod
    def validate_null_values(df: pd.DataFrame) -> bool:
        return not df[
            OHLCVValidator.REQUIRED_COLUMNS
        ].isnull().values.any()

    @staticmethod
    def validate_negative_values(df: pd.DataFrame) -> bool:
        return (
            (df["Open"] >= 0).all()
            and (df["High"] >= 0).all()
            and (df["Low"] >= 0).all()
            and (df["Close"] >= 0).all()
            and (df["Volume"] >= 0).all()
        )

    @staticmethod
    def validate_duplicates(df: pd.DataFrame) -> bool:
        return not df.index.duplicated().any()

    @classmethod
    def validate(cls, df: pd.DataFrame) -> bool:
        return all([
            cls.validate_empty(df),
            cls.validate_required_columns(df),
            cls.validate_null_values(df),
            cls.validate_negative_values(df),
            cls.validate_duplicates(df),
        ])