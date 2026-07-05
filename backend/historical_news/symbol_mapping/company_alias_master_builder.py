from pathlib import Path

import pandas as pd

from historical_news.symbol_mapping.alias_generator import (
    AliasGenerator,
)


class CompanyAliasMasterBuilder:

    def __init__(
        self,
        company_master_file: str,
        output_file: str,
    ):
        self.company_master_file = company_master_file
        self.output_file = output_file

    def build(self) -> pd.DataFrame:

        print(
            f"Loading company master: "
            f"{self.company_master_file}"
        )

        df = pd.read_csv(
            self.company_master_file
        )

        rows = []

        total_companies = len(df)

        for index, row in enumerate(
            df.itertuples(index=False),
            start=1,
        ):

            symbol = row.symbol
            company_name = row.company_name

            aliases = (
                AliasGenerator.generate_aliases(
                    company_name
                )
            )

            for alias in aliases:

                rows.append(
                    {
                        "symbol": symbol,
                        "company_name": company_name,
                        "alias": alias,
                    }
                )

            if index % 100 == 0:

                print(
                    f"Processed "
                    f"{index:,}/{total_companies:,}"
                )

        alias_df = pd.DataFrame(rows)

        alias_df = alias_df.drop_duplicates(
            subset=[
                "symbol",
                "alias",
            ]
        )

        alias_df = alias_df.sort_values(
            by=[
                "symbol",
                "alias",
            ]
        )

        output_path = Path(
            self.output_file
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        alias_df.to_csv(
            output_path,
            index=False,
        )

        print("\n========== SUMMARY ==========")
        print(
            f"Companies : {total_companies:,}"
        )
        print(
            f"Aliases   : {len(alias_df):,}"
        )
        print(
            f"Output    : {output_path}"
        )

        return alias_df


if __name__ == "__main__":

    builder = CompanyAliasMasterBuilder(
        company_master_file=(
            "../datasets/company_master/"
            "company_master.csv"
        ),
        output_file=(
            "../datasets/company_master/"
            "company_alias_master.csv"
        ),
    )

    builder.build()