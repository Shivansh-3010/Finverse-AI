import pandas as pd

from feature_store.technical.technical_features import (
    generate_technical_features,
)

rows = 60

data = pd.DataFrame({
    "high": [100 + i + 1 for i in range(rows)],
    "low": [100 + i - 1 for i in range(rows)],
    "close": [100 + i for i in range(rows)],
    "volume": [100000 + (i * 1000) for i in range(rows)],
})

features = generate_technical_features(data)

for key, value in features.items():
    print(f"{key}: {value}")