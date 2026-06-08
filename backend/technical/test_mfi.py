import pandas as pd

from technical.volume.mfi import calculate_mfi

rows = 60

data = pd.DataFrame({
    "high": [100 + i + 1 for i in range(rows)],
    "low": [100 + i - 1 for i in range(rows)],
    "close": [100 + i for i in range(rows)],
    "volume": [100000 + (i * 1000) for i in range(rows)],
})

result = calculate_mfi(data)

print(result.tail())