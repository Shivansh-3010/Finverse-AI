import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import joblib
import argparse

def predict(
    symbol: str = "RELIANCE",
    horizon: str = "1d",
):

    model_path = (
        PROJECT_ROOT
        / "models"
        / "prophet"
        / f"{symbol}_{horizon}.joblib"
    )

    model = joblib.load(model_path)
    
    print(model.history[["ds", "y"]].tail())

    future = model.make_future_dataframe(
        periods=1,
        freq="D",
    )
    
    print(future.tail())

    forecast = model.predict(future)

    prediction = forecast.iloc[-1]

    return {
        "symbol": symbol,
        "horizon": horizon,
        "prediction": float(prediction["yhat"]),
        "lower": float(prediction["yhat_lower"]),
        "upper": float(prediction["yhat_upper"]),
        "timestamp": str(prediction["ds"]),
    }


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

    print(
        predict(
            symbol=args.symbol,
            horizon=args.horizon,
        )
    )