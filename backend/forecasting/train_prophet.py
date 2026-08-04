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
import argparse

from forecasting.prophet_engine import ProphetEngine
from forecasting.training_pipeline import TrainingPipeline
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)

import numpy as np

from mlops.registry.model_registry import (
    ModelRegistry,
)


def train(
    symbol: str = "RELIANCE",
    horizon: str = "1d",
):

    dataset = TrainingPipeline.build_dataset(
        symbol=symbol,
        horizon=horizon,
    )
    
    print(dataset[["timestamp", "close", "target"]].tail(10))

    prophet_df = (
        dataset.rename(
            columns={
                "timestamp": "ds",
                "target": "y",
            }
        )
    )

    # Prophet requires timezone-naive datetimes
    prophet_df["ds"] = (
        pd.to_datetime(
            prophet_df["ds"]
        )
        .dt.tz_localize(None)
    )

    # Keep only rows where all required features exist
    prophet_df = prophet_df.dropna(
        subset=["ds", "y"]
    )

    model = ProphetEngine.build_model()
    
    print("\n=== Prophet Training Data ===")
    print(prophet_df[["ds", "y"]].tail())
    print(f"Rows: {len(prophet_df)}")
    print(f"Min date: {prophet_df['ds'].min()}")
    print(f"Max date: {prophet_df['ds'].max()}")

    model.fit(prophet_df)

    forecast = model.predict(
        prophet_df[["ds"]]
    )

    y_true = prophet_df["y"].to_numpy()

    y_pred = forecast["yhat"].to_numpy()

    mae = mean_absolute_error(
        y_true,
        y_pred,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred,
        )
    )

    mape = (
        np.mean(
            np.abs(
                (
                    y_true - y_pred
                )
                / np.where(
                    y_true == 0,
                    1,
                    y_true,
                )
            )
        )
        * 100
    )

    directional_accuracy = (
        (
            np.sign(
                np.diff(y_true)
            )
            ==
            np.sign(
                np.diff(y_pred)
            )
        )
        .mean()
        * 100
    )

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
    
    ModelRegistry.register(
        model_name="prophet",
        symbol=symbol,
        horizon=horizon,
        version=f"{horizon}-v1",
        artifact_path=str(model_path),
        metrics={
            "mae": float(mae),
            "rmse": float(rmse),
            "mape": float(mape),
            "directional_accuracy": float(
                directional_accuracy
            ),
        },
    )

    print(
        f"Saved Prophet model -> {model_path}"
    )
    
    print()

    print(
        "MAE:",
        round(mae, 4),
    )

    print(
        "RMSE:",
        round(rmse, 4),
    )

    print(
        "MAPE:",
        round(mape, 4),
    )

    print(
        "Directional Accuracy:",
        round(
            directional_accuracy,
            2,
        ),
        "%",
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--symbol",
        default="RELIANCE",
    )

    parser.add_argument(
        "--horizon",
        default="1d",
    )

    args = parser.parse_args()

    train(
        symbol=args.symbol,
        horizon=args.horizon,
    )