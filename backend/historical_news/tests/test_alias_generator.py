import pandas as pd

from historical_news.symbol_mapping.alias_generator import (
    AliasGenerator,
)


df = pd.read_csv(
    "../datasets/company_master/company_master.csv"
)

symbols = [
    "RELIANCE",
    "INFY",
    "TCS",
    "SBIN",
    "HDFCBANK",
]

for symbol in symbols:

    company_name = df.loc[
        df["symbol"] == symbol,
        "company_name",
    ].iloc[0]

    aliases = AliasGenerator.generate_aliases(
        company_name
    )

    print("\n" + "=" * 50)
    print(symbol)
    print(company_name)
    print()

    for alias in aliases:
        print(alias)