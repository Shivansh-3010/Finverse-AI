from historical_news.symbol_mapping.symbol_universe import (
    SymbolUniverse,
)


def test_symbol_universe():

    symbols = SymbolUniverse.load_symbols(
        "../datasets/OHLCV/NSE-stock-market-historical-data/v1"
    )

    print(f"\nSymbols found: {len(symbols):,}")

    print("First 20 symbols:")

    print(symbols[:20])

    assert "RELIANCE" in symbols

    assert len(symbols) > 1500