import pandas as pd


def ohlcv_to_dataframe(records):

    return pd.DataFrame([
        {
            "high": record.high,
            "low": record.low,
            "close": record.close,
            "volume": record.volume,
        }
        for record in records
    ])