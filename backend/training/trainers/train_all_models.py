import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import pandas as pd

from database.session import SessionLocal
from repositories.ohlcv_repository import OHLCVRepository

from forecasting.train_xgboost import train
from forecasting.horizons import SUPPORTED_HORIZONS


RESULTS_FILE = "models/training_results.csv"


def save_results(results):

    pd.DataFrame(results).to_csv(
        RESULTS_FILE,
        index=False,
    )


def train_all_models():

    db = SessionLocal()

    try:

        symbols = (
            OHLCVRepository(db)
            .get_all_symbols()
        )

    finally:

        db.close()

    total_jobs = (
        len(symbols)
        * len(SUPPORTED_HORIZONS)
    )

    completed_jobs = 0

    results = []

    print("\n" + "=" * 80)
    print("FINVERSE BULK TRAINING")
    print("=" * 80)
    print(f"Symbols : {len(symbols)}")
    print(f"Horizons: {SUPPORTED_HORIZONS}")
    print(f"Total Jobs: {total_jobs}")
    print("=" * 80)

    for symbol in symbols:

        for horizon in SUPPORTED_HORIZONS:

            model_path = Path(
                f"models/xgboost/"
                f"{symbol.lower()}_xgb_{horizon}.pkl"
            )

            if model_path.exists():

                completed_jobs += 1

                print(
                    f"[{completed_jobs}/{total_jobs}] "
                    f"SKIP {symbol} {horizon}"
                )

                results.append(
                    {
                        "symbol": symbol,
                        "horizon": horizon,
                        "status": "SKIPPED",
                    }
                )

                save_results(results)

                continue

            try:

                completed_jobs += 1

                print(
                    f"\n[{completed_jobs}/{total_jobs}] "
                    f"TRAIN {symbol} {horizon}"
                )

                result = train(
                    symbol=symbol,
                    horizon=horizon,
                )

                result["status"] = "SUCCESS"

                results.append(result)

                save_results(results)

                print(result)

            except Exception as e:

                print(
                    f"\nFAILED: "
                    f"{symbol} {horizon}"
                )

                print(str(e))

                results.append(
                    {
                        "symbol": symbol,
                        "horizon": horizon,
                        "status": "FAILED",
                        "error": str(e),
                    }
                )

                save_results(results)

                continue

    print("\n" + "=" * 80)
    print("TRAINING COMPLETE")
    print("=" * 80)

    success_count = len(
        [
            r for r in results
            if r.get("status") == "SUCCESS"
        ]
    )

    failed_count = len(
        [
            r for r in results
            if r.get("status") == "FAILED"
        ]
    )

    skipped_count = len(
        [
            r for r in results
            if r.get("status") == "SKIPPED"
        ]
    )

    print(f"Success : {success_count}")
    print(f"Failed  : {failed_count}")
    print(f"Skipped : {skipped_count}")
    print(f"Results : {RESULTS_FILE}")


if __name__ == "__main__":

    train_all_models()