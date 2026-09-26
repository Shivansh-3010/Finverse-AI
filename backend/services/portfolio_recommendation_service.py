from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_risk_score_service import (
    portfolio_risk_score_service,
)
from services.portfolio_drawdown_service import (
    portfolio_drawdown_service,
)
from services.portfolio_liquidity_service import (
    portfolio_liquidity_service,
)
from services.portfolio_diversification_service import (
    portfolio_diversification_service,
)
from services.portfolio_rebalancing_service import (
    portfolio_rebalancing_service,
)
from services.portfolio_risk_adjusted_return_service import (
    portfolio_risk_adjusted_return_service,
)


class PortfolioRecommendationService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        benchmark: str = "NIFTY50",
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        risk = portfolio_risk_score_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            benchmark=benchmark,
            timeframe=timeframe,
            lookback_days=lookback_days,
        )

        drawdown = portfolio_drawdown_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
            lookback_days=lookback_days,
        )

        liquidity = portfolio_liquidity_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
        )

        diversification = (
            portfolio_diversification_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        rebalancing = (
            portfolio_rebalancing_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                benchmark=benchmark,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        risk_adjusted = (
            portfolio_risk_adjusted_return_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        recommendations = []

        risk_score_raw = risk.get(
            "overall_risk_score"
        )

        if risk_score_raw is not None:
            risk_score = Decimal(
                str(risk_score_raw)
            )

            if risk_score >= Decimal("70"):
                recommendations.append(
                    {
                        "action": "REDUCE_RISK",
                        "priority": "HIGH",
                        "reason":
                            "Portfolio risk score is elevated",
                    }
                )
            elif risk_score >= Decimal("50"):
                recommendations.append(
                    {
                        "action": "MONITOR_RISK",
                        "priority": "MEDIUM",
                        "reason":
                            "Portfolio risk is moderately elevated",
                    }
                )

        diversification_score = diversification.get(
            "diversification_score"
        )

        if diversification_score is not None:
            if Decimal(
                str(diversification_score)
            ) < Decimal("40"):
                recommendations.append(
                    {
                        "action": "DIVERSIFY",
                        "priority": "HIGH",
                        "reason":
                            "Portfolio diversification is weak",
                    }
                )

        drawdown_value = drawdown.get(
            "current_drawdown_pct"
        )

        if drawdown_value is not None:
            if abs(
                Decimal(str(drawdown_value))
            ) >= Decimal("10"):
                recommendations.append(
                    {
                        "action": "REVIEW_DRAWDOWN",
                        "priority": "HIGH",
                        "reason":
                            "Portfolio is experiencing a significant drawdown",
                    }
                )

        liquidity_score = liquidity.get(
            "portfolio_liquidity_score"
        )

        if liquidity_score is not None:
            if Decimal(
                str(liquidity_score)
            ) < Decimal("40"):
                recommendations.append(
                    {
                        "action": "IMPROVE_LIQUIDITY",
                        "priority": "HIGH",
                        "reason":
                            "Portfolio liquidity is elevated-risk",
                    }
                )

        if rebalancing.get(
            "rebalancing_required"
        ):
            recommendations.append(
                {
                    "action": "REBALANCE",
                    "priority": "MEDIUM",
                    "reason":
                        "Current allocation differs materially from target allocation",
                }
            )

        performance_category = (
            risk_adjusted.get(
                "performance_category"
            )
        )

        if performance_category == (
            "Poor Risk-Adjusted Performance"
        ):
            recommendations.append(
                {
                    "action": "REVIEW_PERFORMANCE",
                    "priority": "MEDIUM",
                    "reason":
                        "Portfolio return is weak relative to observed downside risk",
                }
            )

        if not recommendations:
            recommendations.append(
                {
                    "action": "HOLD",
                    "priority": "LOW",
                    "reason":
                        "No major portfolio action is currently indicated",
                }
            )

        priority_rank = {
            "HIGH": 0,
            "MEDIUM": 1,
            "LOW": 2,
        }

        recommendations.sort(
            key=lambda item:
                priority_rank.get(
                    item["priority"],
                    3,
                )
        )

        return {
            "portfolio_id": portfolio_id,
            "benchmark": benchmark,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "recommendation_count":
                len(recommendations),
            "recommendations":
                recommendations,
            "risk_category":
                risk.get("risk_category"),
            "diversification_category":
                diversification.get(
                    "diversification_category"
                ),
            "liquidity_category":
                liquidity.get(
                    "liquidity_category"
                ),
            "rebalancing_required":
                rebalancing.get(
                    "rebalancing_required"
                ),
            "message": None,
        }


portfolio_recommendation_service = (
    PortfolioRecommendationService()
)