from datetime import datetime
from typing import Optional

from twelvedata import TDClient

from core.settings import settings


class BenchmarkDataProvider:

    BENCHMARKS = {
        "NIFTY50": "NIFTY 50",
        "SENSEX": "BSE SENSEX",
    }

    def __init__(self):
        if not settings.TWELVE_DATA_API_KEY:
            raise ValueError(
                "TWELVE_DATA_API_KEY is not configured"
            )

        self.client = TDClient(
            apikey=settings.TWELVE_DATA_API_KEY
        )

    def get_daily_data(
        self,
        benchmark: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        benchmark = benchmark.upper()

        if benchmark not in self.BENCHMARKS:
            raise ValueError(
                f"Unsupported benchmark: {benchmark}. "
                f"Supported: {list(self.BENCHMARKS.keys())}"
            )

        symbol = self.BENCHMARKS[benchmark]

        query = self.client.time_series(
            symbol=symbol,
            interval="1day",
            outputsize=5000,
            start_date=start_date,
            end_date=end_date,
        )

        df = query.as_pandas()

        if df is None or df.empty:
            return df

        df = df.reset_index()

        df.columns = [
            str(column).lower()
            for column in df.columns
        ]

        if "datetime" in df.columns:
            df.rename(
                columns={"datetime": "timestamp"},
                inplace=True
            )

        if "date" in df.columns:
            df.rename(
                columns={"date": "timestamp"},
                inplace=True
            )

        df["symbol"] = benchmark
        df["timeframe"] = "1d"

        return df[
            [
                "symbol",
                "timeframe",
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        ].sort_values("timestamp")