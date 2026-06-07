import pandas as pd

from technical.trend.adx import calculate_adx


rows = 60

data = pd.DataFrame({
    "high": [100 + i + 1 for i in range(rows)],
    "low": [100 + i - 1 for i in range(rows)],
    "close": [100 + i for i in range(rows)],
})

result = calculate_adx(data)

print(result.tail())