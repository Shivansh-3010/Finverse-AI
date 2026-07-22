import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import joblib
import pandas as pd

from forecasting.prophet_engine import ProphetEngine
from forecasting.training_pipeline import TrainingPipeline


def train(
    symbol: str = "RELIANCE",
    horizon: str = "1d",
):

    dataset = TrainingPipeline.build_dataset(
        symbol=symbol,
        horizon=horizon,
    )

    prophet_df = (
        dataset[
            ["timestamp", "target"]
        ]
        .rename(
            columns={
                "timestamp": "ds",
                "target": "y",
            }
        )
        .dropna()
    )

    # Prophet requires timezone-naive datetimes
    prophet_df["ds"] = (
        pd.to_datetime(
            prophet_df["ds"]
        )
        .dt.tz_localize(None)
    )

    model = ProphetEngine.build_model()

    model.fit(prophet_df)

    output_dir = (
        PROJECT_ROOT
        / "models"
        / "prophet"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_path = (
        output_dir
        / f"{symbol}_{horizon}.joblib"
    )

    joblib.dump(
        model,
        model_path,
    )

    print(
        f"Saved Prophet model -> {model_path}"
    )


if __name__ == "__main__":
    train()