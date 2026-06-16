import yfinance as yf
import pandas as pd


class YahooIngestor:
    """Fetch market data from Yahoo Finance."""

    def __init__(self):
        pass

    def get_historical_data(
        self,
        symbol: str,
        period: str = "1y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV data.
        """

        ticker = yf.Ticker(symbol)

        df = ticker.history(
            period=period,
            interval=interval
        )

        return df
    
    def get_company_name(
        self,
        symbol: str
    ) -> str:

        try:

            ticker = yf.Ticker(
                f"{symbol}.NS"
            )

            info = ticker.info

            return (
                info.get(
                    "longName"
                )
                or
                symbol
            )

        except Exception:

            return symbol