from datetime import datetime, timezone

import pandas as pd
from twelvedata import TDClient


class TwelveDataProvider:
    """Wrapper around Twelve Data for historical market data."""

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError(
                "Twelve Data API key is not configured."
            )

        self.client = TDClient(
            apikey=api_key
        )

    def get_historical_data(
        self,
        symbol: str,
        interval: str = "1day",
        outputsize: int = 5000,
    ) -> pd.DataFrame:

        response = (
            self.client.time_series(
                symbol=symbol,
                interval=interval,
                outputsize=outputsize,
                order="ASC",
            )
            .as_pandas()
        )

        if response is None or response.empty:
            return pd.DataFrame()

        response = response.reset_index()

        response.columns = [
            str(column).lower()
            for column in response.columns
        ]

        if "datetime" in response.columns:
            response["datetime"] = pd.to_datetime(
                response["datetime"],
                utc=True,
            )

        return response