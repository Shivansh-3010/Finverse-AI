import pandas as pd

from agents.risk_analysis_agent.agent import (
    RiskAnalysisAgent
)


def test_risk_analysis_agent():

    prices = pd.Series(
        [100, 102, 101, 105, 103, 99, 95, 90]
    )

    result = RiskAnalysisAgent.analyze(
        prices
    )

    assert "volatility" in result
    assert "drawdown" in result
    assert "var_95" in result
    assert "expected_shortfall" in result
    assert "risk_score" in result
    assert "risk_category" in result


def test_risk_score_range():

    prices = pd.Series(
        [100, 102, 101, 105, 103, 99, 95, 90]
    )

    result = RiskAnalysisAgent.analyze(
        prices
    )

    assert (
        0 <= result["risk_score"] <= 100
    )