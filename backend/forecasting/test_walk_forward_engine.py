import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))
    
import pandas as pd

from forecasting.walk_forward_engine import (
    WalkForwardEngine,
)


def train_callback(
    train_df,
):

    return {
        "mean": train_df[
            "value"
        ].mean()
    }


def predict_callback(
    model,
    test_df,
):

    return [
        model["mean"]
    ] * len(test_df)


def test():

    df = pd.DataFrame(
        {
            "value": range(100),
            "target": range(100),
        }
    )

    result = (
        WalkForwardEngine.run(
            dataset=df,
            train_size=60,
            test_size=20,
            step_size=10,
            train_callback=train_callback,
            predict_callback=predict_callback,
        )
    )

    assert result["windows"] == 3
    assert len(result["results"]) == 3

    print(result)


if __name__ == "__main__":
    test()