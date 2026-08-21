import pandas as pd

from sqlalchemy.orm import Session
from uuid import UUID

from repositories.portfolio_snapshot_repository import (
    portfolio_snapshot_repository,
)

from risk.volatility_engine import VolatilityEngine
from risk.drawdown_engine import DrawdownEngine
from risk.var_engine import ValueAtRiskEngine
from risk.expected_shortfall_engine import (
    ExpectedShortfallEngine,
)
from risk.risk_score_engine import RiskScoreEngine


class PortfolioRiskService:
    """
    Calculate portfolio-level risk metrics from
    historical portfolio snapshots.
    """

    MIN_SNAPSHOTS = 30

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
    ) -> dict:

        snapshots = (
            portfolio_snapshot_repository.get_by_portfolio(
                db,
                portfolio_id,
            )
        )

        if len(snapshots) < PortfolioRiskService.MIN_SNAPSHOTS:
            return {
                "portfolio_id": portfolio_id,
                "snapshot_count": len(snapshots),
                "sufficient_history": False,
                "volatility": None,
                "drawdown": None,
                "var_95": None,
                "expected_shortfall": None,
                "risk_score": None,
                "risk_category": "Insufficient Data",
                "reason": (
                    "At least 30 portfolio snapshots "
                    "are required to calculate reliable risk metrics."
                ),
            }

        portfolio_values = pd.Series(
            [
                float(snapshot.portfolio_value)
                for snapshot in snapshots
            ],
            dtype="float64",
        )

        returns = (
            VolatilityEngine.calculate_returns(
                portfolio_values
            )
        )

        if returns.empty:
            return {
                "portfolio_id": portfolio_id,
                "snapshot_count": len(snapshots),
                "sufficient_history": False,
                "volatility": None,
                "drawdown": None,
                "var_95": None,
                "expected_shortfall": None,
                "risk_score": None,
                "risk_category": "Insufficient Data",
                "reason": (
                    "Portfolio snapshots do not contain "
                    "enough return observations."
                ),
            }

        volatility = (
            VolatilityEngine.annualized_volatility(
                portfolio_values
            ) * 100
        )

        drawdown = (
            DrawdownEngine.max_drawdown(
                portfolio_values
            )
        )

        var_95 = (
            ValueAtRiskEngine.calculate_var(
                portfolio_values
            )
        )

        expected_shortfall = (
            ExpectedShortfallEngine
            .calculate_expected_shortfall(
                portfolio_values
            )
        )

        risk_score = (
            RiskScoreEngine.calculate_score(
                volatility=volatility,
                drawdown=drawdown,
                var_95=var_95,
                expected_shortfall=expected_shortfall,
            )
        )

        risk_category = (
            RiskScoreEngine.classify_risk(
                risk_score
            )
        )

        return {
            "portfolio_id": portfolio_id,
            "snapshot_count": len(snapshots),
            "sufficient_history": True,
            "volatility": round(
                volatility,
                2,
            ),
            "drawdown": round(
                drawdown,
                2,
            ),
            "var_95": round(
                var_95,
                2,
            ),
            "expected_shortfall": round(
                expected_shortfall,
                2,
            ),
            "risk_score": risk_score,
            "risk_category": risk_category,
        }


portfolio_risk_service = PortfolioRiskService()