from pathlib import Path
import re
from typing import Dict, List, Set

import pandas as pd


class NewsSymbolMapper:

    def __init__(
        self,
        alias_master_file: str,
        news_file: str,
        output_file: str,
        chunk_size: int = 10000,
    ):
        self.alias_master_file = alias_master_file
        self.news_file = news_file
        self.output_file = output_file
        self.chunk_size = chunk_size

        self.alias_patterns = []

    def load_aliases(self) -> None:

        print(
            f"Loading aliases from: "
            f"{self.alias_master_file}"
        )

        alias_df = pd.read_csv(
            self.alias_master_file
        )

        alias_df = alias_df.drop_duplicates(
            subset=["alias", "symbol"]
        )

        alias_df["alias_length"] = (
            alias_df["alias"]
            .astype(str)
            .str.len()
        )

        alias_df = alias_df.sort_values(
            by="alias_length",
            ascending=False,
        )

        patterns = []

        for row in alias_df.itertuples():

            alias = str(row.alias).strip()

            if not alias:
                continue

            pattern = re.compile(
                rf"\b{re.escape(alias)}\b",
                flags=re.IGNORECASE,
            )

            patterns.append(
                (
                    alias,
                    row.symbol,
                    pattern,
                )
            )

        self.alias_patterns = patterns

        print(
            f"Loaded "
            f"{len(self.alias_patterns):,} "
            f"alias patterns"
        )

    def map_article(
        self,
        title: str,
        description: str,
    ) -> List[str]:

        title = "" if pd.isna(title) else str(title)
        description = (
            ""
            if pd.isna(description)
            else str(description)
        )

        search_text = (
            title + " " + description
        )

        matched_symbols: Set[str] = set()

        for _, symbol, pattern in self.alias_patterns:

            if pattern.search(search_text):

                matched_symbols.add(symbol)

        return sorted(matched_symbols)

    def process_chunk(
        self,
        chunk: pd.DataFrame,
    ) -> pd.DataFrame:

        mapped_symbols = []

        for row in chunk.itertuples():

            symbols = self.map_article(
                getattr(row, "title", ""),
                getattr(row, "description", ""),
            )

            mapped_symbols.append(
                ",".join(symbols)
            )

        chunk = chunk.copy()

        chunk["symbols"] = mapped_symbols

        return chunk

    def build(self) -> pd.DataFrame:

        self.load_aliases()

        print(
            f"Loading news from: "
            f"{self.news_file}"
        )

        news_df = pd.read_csv(
            self.news_file
        )

        total_rows = len(news_df)

        print(
            f"News records: "
            f"{total_rows:,}"
        )

        output_chunks = []

        mapped_articles = 0

        for start in range(
            0,
            total_rows,
            self.chunk_size,
        ):

            end = min(
                start + self.chunk_size,
                total_rows,
            )

            print(
                f"Processing "
                f"{start:,} - {end:,}"
            )

            chunk = news_df.iloc[start:end]

            processed_chunk = (
                self.process_chunk(chunk)
            )

            mapped_articles += (
                processed_chunk["symbols"]
                .ne("")
                .sum()
            )

            output_chunks.append(
                processed_chunk
            )

            # checkpoint save
            temp_df = pd.concat(
                output_chunks,
                ignore_index=True,
            )

            Path(
                self.output_file
            ).parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            temp_df.to_csv(
                self.output_file,
                index=False,
            )

            print(
                f"Checkpoint saved "
                f"({end:,}/{total_rows:,})"
            )

        result_df = pd.concat(
            output_chunks,
            ignore_index=True,
        )

        result_df.to_csv(
            self.output_file,
            index=False,
        )

        print("\n========== SUMMARY ==========")
        print(
            f"News Records    : "
            f"{len(result_df):,}"
        )
        print(
            f"Mapped Articles : "
            f"{mapped_articles:,}"
        )
        print(
            f"Coverage        : "
            f"{(mapped_articles / len(result_df)) * 100:.2f}%"
        )
        print(
            f"Output          : "
            f"{self.output_file}"
        )

        return result_df


if __name__ == "__main__":

    mapper = NewsSymbolMapper(
        alias_master_file=(
            "../datasets/company_master/"
            "company_alias_master.csv"
        ),
        news_file=(
            "../datasets/historical_news_processed/"
            "historical_news_v1.csv"
        ),
        output_file=(
            "../datasets/historical_news_processed/"
            "historical_news_symbol_mapped.csv"
        ),
        chunk_size=10000,
    )

    mapper.build()