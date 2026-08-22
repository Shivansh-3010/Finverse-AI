from __future__ import annotations

import pandas as pd
import yfinance as yf


class BenchmarkDataService:

    BENCHMARKS = {
        "NIFTY50": "^NSEI",
        "SENSEX": "^BSESN",
    }

    def get_history(
        self,
        benchmark: str,
        period: str = "1y",
        interval: str = "1d",
    ) -> list[dict]:

        benchmark = benchmark.upper()

        if benchmark not in self.BENCHMARKS:
            raise ValueError(
                f"Unsupported benchmark: {benchmark}. "
                f"Supported: {list(self.BENCHMARKS)}"
            )

        ticker = self.BENCHMARKS[benchmark]

        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False,
        )

        if df.empty:
            return []

        # yfinance may return MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()

        df = df.rename(
            columns={
                "Date": "timestamp",
                "Datetime": "timestamp",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )

        required = [
            "timestamp",
            "open",
            "high",
            "low",
            "close",
        ]

        df = df.dropna(subset=required)

        records = []

        for _, row in df.iterrows():
            records.append(
                {
                    "benchmark": benchmark,
                    "symbol": ticker,
                    "timestamp": pd.to_datetime(
                        row["timestamp"],
                        utc=True,
                    ),
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": int(
                        row["volume"]
                    )
                    if pd.notna(row.get("volume"))
                    else 0,
                }
            )

        return records


benchmark_data_service = BenchmarkDataService()