from risk.risk_score_engine import RiskScoreEngine


def test_risk_score_calculation():

    score = RiskScoreEngine.calculate_score(
        volatility=25,
        drawdown=-15,
        var_95=8,
        expected_shortfall=12
    )

    assert isinstance(score, int)
    assert 0 <= score <= 100


def test_risk_classification():

    assert RiskScoreEngine.classify_risk(10) == "Very Low Risk"
    assert RiskScoreEngine.classify_risk(30) == "Low Risk"
    assert RiskScoreEngine.classify_risk(50) == "Moderate Risk"
    assert RiskScoreEngine.classify_risk(70) == "High Risk"
    assert RiskScoreEngine.classify_risk(90) == "Very High Risk"