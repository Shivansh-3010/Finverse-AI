import pandas as pd

from agents.technical_analysis_agent.agent import TechnicalAnalysisAgent


data = pd.DataFrame({
    "close": [
        100, 101, 102, 103, 104,
        105, 106, 107, 108, 109,
        110, 111, 112, 113, 114,
        115, 116, 117, 118, 119,
        120, 121, 122, 123, 124
    ]
})

agent = TechnicalAnalysisAgent()

result = agent.analyze(data)

print(result)