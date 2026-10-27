from types import SimpleNamespace

from agents.candlestick_analysis_agent.agent import CandlestickAnalysisAgent


def test_analyze_returns_candlestick_analysis():
    records = [
        SimpleNamespace(
            open=100.0,
            high=102.0,
            low=99.0,
            close=101.0,
            volume=1000.0,
        )
    ]

    result = CandlestickAnalysisAgent().analyze(records)

    assert isinstance(result, dict)
    assert "candlestick_score" in result
    assert "patterns" in result
    assert isinstance(result["patterns"], list)
