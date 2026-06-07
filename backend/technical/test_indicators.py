import pandas as pd

from technical.trend.sma import calculate_sma
from technical.trend.ema import calculate_ema
from technical.momentum.rsi import calculate_rsi


data = pd.DataFrame({
    "close": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
              110, 111, 112, 113, 114, 115, 116, 117, 118, 119,
              120, 121, 122, 123, 124]
})

print("SMA:")
print(calculate_sma(data).tail())

print("\nEMA:")
print(calculate_ema(data).tail())

print("\nRSI:")
print(calculate_rsi(data).tail())