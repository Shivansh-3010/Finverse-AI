import pandas as pd

from agents.support_resistance_agent.agent import (
    SupportResistanceAgent,
)


data = {
    "high": [
        120,
        125,
        130,
        127,
        122,
        118,
        123,
        128,
        132,
        129,
        124,
    ],
    "low": [
        115,
        120,
        125,
        122,
        118,
        110,
        116,
        121,
        126,
        123,
        119,
    ],
    "close": [
        118,
        124,
        128,
        125,
        120,
        112,
        121,
        126,
        130,
        127,
        124,
    ]
}

df = pd.DataFrame(data)

agent = SupportResistanceAgent()

result = agent.analyze(
    data=df,
    current_price=124,
)

print(result)