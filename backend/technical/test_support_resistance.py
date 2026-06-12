import pandas as pd

from technical.support_resistance.support_resistance_analysis import (
    analyze_support_resistance,
)

data = {
    "high": [
        100,
        110,
        120,
        110,
        100,
        105,
        115,
        125,
    ],
    "low": [
        95,
        100,
        105,
        100,
        95,
        100,
        110,
        120,
    ],
    "close": [
        98,
        108,
        118,
        108,
        98,
        104,
        118,
        126,
    ],
}

df = pd.DataFrame(data)

result = analyze_support_resistance(
    df=df,
    current_price=126,
)

print(result)