from agents.candlestick_analysis_agent.agent import (
    CandlestickAnalysisAgent,
)


agent = CandlestickAnalysisAgent()

result = agent.analyze(
    open_price=100,
    high_price=102,
    low_price=90,
    close_price=101,
)

print(result)