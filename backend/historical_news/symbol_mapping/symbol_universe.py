from pathlib import Path


class SymbolUniverse:

    @staticmethod
    def load_symbols(
        directory_path: str,
    ) -> list[str]:

        directory = Path(directory_path)

        symbols = []

        for file in directory.glob("*.csv"):

            symbol = file.stem.upper()

            symbol = symbol.replace(".NS", "")

            symbols.append(symbol)

        return sorted(symbols)