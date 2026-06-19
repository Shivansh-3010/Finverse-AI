import pandas as pd
import numpy as np

from forecasting.dataset_builder import (
    DatasetBuilder,
)

rows = 50

df = pd.DataFrame(
    {
        "timestamp": range(rows),
        "close": np.arange(
            100,
            100 + rows
        ),
        "high": np.arange(
            101,
            101 + rows
        ),
        "low": np.arange(
            99,
            99 + rows
        ),
        "volume": [1000] * rows,
    }
)

dataset = DatasetBuilder.build(
    df,
    horizon_days=3,
)

print(
    dataset[
        ["close", "target"]
    ].head()
)