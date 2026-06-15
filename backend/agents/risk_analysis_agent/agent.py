import pandas as pd

from risk.volatility_engine import VolatilityEngine
from risk.drawdown_engine import DrawdownEngine
from risk.var_engine import ValueAtRiskEngine
from risk.expected_shortfall_engine import ExpectedShortfallEngine
from risk.risk_score_engine import RiskScoreEngine
from risk.risk_explainability import (
    RiskExplainability
)

class RiskAnalysisAgent:
    """
    Central Risk Intelligence Agent.
    """

    @staticmethod
    def analyze(close_prices: pd.Series) -> dict:

        annualized_volatility = (
            VolatilityEngine.annualized_volatility(
                close_prices
            ) * 100
        )

        drawdown = DrawdownEngine.max_drawdown(
            close_prices
        )

        var_95 = ValueAtRiskEngine.calculate_var(
            close_prices
        )

        expected_shortfall = (
            ExpectedShortfallEngine
            .calculate_expected_shortfall(
                close_prices
            )
        )

        risk_score = (
            RiskScoreEngine.calculate_score(
                volatility=annualized_volatility,
                drawdown=drawdown,
                var_95=var_95,
                expected_shortfall=expected_shortfall
            )
        )

        return {
            "volatility": round(
                annualized_volatility, 2
            ),
            "drawdown": round(
                drawdown, 2
            ),
            "var_95": round(
                var_95, 2
            ),
            "expected_shortfall": round(
                expected_shortfall, 2
            ),
            "risk_score": risk_score,
            "risk_category":
                RiskScoreEngine.classify_risk(
                    risk_score
            ),
            "reason": (
                RiskExplainability.explain(
                    volatility=annualized_volatility,
                    drawdown=drawdown,
                    risk_score=risk_score
                )
            )
        }