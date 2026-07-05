from pathlib import Path
from time import sleep

import pandas as pd
import yfinance as yf

from historical_news.symbol_mapping.symbol_universe import (
    SymbolUniverse,
)


class CompanyMasterBuilder:

    def __init__(
        self,
        ohlcv_directory: str,
        output_file: str,
    ):
        self.ohlcv_directory = ohlcv_directory
        self.output_file = output_file

    def build(self) -> pd.DataFrame:

        symbols = SymbolUniverse.load_symbols(
            self.ohlcv_directory
        )

        print(f"Found {len(symbols):,} symbols")

        rows = []

        success_count = 0
        failed_count = 0

        for index, symbol in enumerate(symbols, start=1):

            yahoo_symbol = f"{symbol}.NS"

            try:

                print(
                    f"[{index}/{len(symbols)}] "
                    f"Fetching {yahoo_symbol}"
                )

                ticker = yf.Ticker(yahoo_symbol)

                info = ticker.info

                company_name = (
                    info.get("longName")
                    or info.get("shortName")
                )

                sector = info.get("sector")
                industry = info.get("industry")

                if not company_name:

                    print(
                        f"  -> Missing company name "
                        f"for {yahoo_symbol}"
                    )

                    failed_count += 1

                    continue

                rows.append(
                    {
                        "symbol": symbol,
                        "yahoo_symbol": yahoo_symbol,
                        "company_name": company_name,
                        "sector": sector,
                        "industry": industry,
                    }
                )

                success_count += 1
                
                if len(rows) % 100 == 0:

                    pd.DataFrame(rows).to_csv(
                        self.output_file,
                        index=False,
                    )

                    print(
                        f"Checkpoint saved "
                        f"({len(rows):,} records)"
                    )

            except Exception as e:

                print(
                    f"  -> Failed {yahoo_symbol}: {e}"
                )

                failed_count += 1

            # be polite to Yahoo
            sleep(0.1)

        df = pd.DataFrame(rows)

        output_path = Path(self.output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_csv(
            output_path,
            index=False,
        )

        print("\n========== SUMMARY ==========")
        print(f"Success : {success_count:,}")
        print(f"Failed  : {failed_count:,}")
        print(f"Saved   : {len(df):,}")
        print(f"Output  : {output_path}")

        return df


if __name__ == "__main__":

    builder = CompanyMasterBuilder(
        ohlcv_directory=(
            "../datasets/OHLCV/"
            "NSE-stock-market-historical-data/v1"
        ),
        output_file=(
            "../datasets/company_master/"
            "company_master.csv"
        ),
    )

    builder.build()