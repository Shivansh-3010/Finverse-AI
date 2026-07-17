import os
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from database.session import SessionLocal
from training.universe.universe_selector import UniverseSelector
from models.candlestick_pattern import CandlestickPattern
from services.historical_candlestick_backfill_service import (
    HistoricalCandlestickBackfillService,
)

PROGRESS_FILE = "scripts/rebuild_progress.txt"

db = SessionLocal()

# --------------------------------------------------
# Load completed symbols
# --------------------------------------------------

completed_symbols = set()

if os.path.exists(PROGRESS_FILE):

    with open(
        PROGRESS_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        completed_symbols = {
            line.strip()
            for line in f
            if line.strip()
        }

print(
    f"FOUND {len(completed_symbols)} "
    f"COMPLETED SYMBOLS"
)

# --------------------------------------------------
# Get symbols
# --------------------------------------------------

symbols = UniverseSelector.get_symbols(
    db,
    timeframe="1d",
    min_candles=50,
)

total_symbols = len(symbols)

print(
    f"TOTAL SYMBOLS: "
    f"{total_symbols}"
)

# --------------------------------------------------
# Process symbols
# --------------------------------------------------

for index, symbol in enumerate(
    symbols,
    start=1,
):

    if symbol in completed_symbols:

        print(
            f"[{index}/{total_symbols}] "
            f"SKIPPED {symbol}"
        )

        continue

    try:

        print(
            f"\n"
            f"[{index}/{total_symbols}] "
            f"PROCESSING {symbol}"
        )

        # ------------------------------------------
        # Remove partial data if previous run died
        # halfway through this symbol
        # ------------------------------------------

        deleted = (
            db.query(CandlestickPattern)
            .filter(
                CandlestickPattern.symbol
                == symbol
            )
            .delete()
        )

        db.commit()

        if deleted > 0:

            print(
                f"Deleted "
                f"{deleted:,} "
                f"partial rows"
            )

        # ------------------------------------------
        # Rebuild symbol
        # ------------------------------------------

        result = (
            HistoricalCandlestickBackfillService
            .backfill_symbol(
                db,
                symbol,
                "1d",
            )
        )

        db.commit()

        print(result)

        # ------------------------------------------
        # Mark complete
        # ------------------------------------------

        with open(
            PROGRESS_FILE,
            "a",
            encoding="utf-8",
        ) as f:

            f.write(
                symbol + "\n"
            )

        completed_symbols.add(
            symbol
        )

        print(
            f"COMPLETED: {symbol}"
        )

    except Exception as e:

        db.rollback()

        print(
            f"FAILED {symbol}: {e}"
        )

print(
    "\n"
    "================================="
)
print("REBUILD COMPLETE")
print(
    f"COMPLETED SYMBOLS: "
    f"{len(completed_symbols)}"
)
print(
    "================================="
)