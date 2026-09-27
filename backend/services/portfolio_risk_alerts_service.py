from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_risk_score_service import (
    portfolio_risk_score_service,
)
from services.portfolio_drawdown_service import (
    portfolio_drawdown_service,
)
from services.portfolio_var_service import (
    portfolio_var_service,
)
from services.portfolio_liquidity_service import (
    portfolio_liquidity_service,
)


class PortfolioRiskAlertsService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        risk_score = (
            portfolio_risk_score_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        drawdown = (
            portfolio_drawdown_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        var_result = (
            portfolio_var_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        liquidity = (
            portfolio_liquidity_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        alerts = []

        overall_risk_raw = risk_score.get(
            "overall_risk_score"
        )

        if overall_risk_raw is not None:
            overall_risk = Decimal(
                str(overall_risk_raw)
            )

            if overall_risk >= Decimal("80"):
                alerts.append(
                    {
                        "alert_type": "OVERALL_RISK",
                        "severity": "CRITICAL",
                        "message": (
                            "Portfolio overall risk is "
                            "critically elevated"
                        ),
                    }
                )

            elif overall_risk >= Decimal("60"):
                alerts.append(
                    {
                        "alert_type": "OVERALL_RISK",
                        "severity": "HIGH",
                        "message": (
                            "Portfolio overall risk is "
                            "elevated"
                        ),
                    }
                )

            elif overall_risk >= Decimal("40"):
                alerts.append(
                    {
                        "alert_type": "OVERALL_RISK",
                        "severity": "MEDIUM",
                        "message": (
                            "Portfolio risk requires "
                            "monitoring"
                        ),
                    }
                )

        drawdown_raw = drawdown.get(
            "current_drawdown_pct"
        )

        if drawdown_raw is not None:
            drawdown_pct = abs(
                Decimal(str(drawdown_raw))
            )

            if drawdown_pct >= Decimal("20"):
                alerts.append(
                    {
                        "alert_type": "DRAWDOWN",
                        "severity": "CRITICAL",
                        "message": (
                            "Portfolio is experiencing "
                            "a severe drawdown"
                        ),
                    }
                )

            elif drawdown_pct >= Decimal("10"):
                alerts.append(
                    {
                        "alert_type": "DRAWDOWN",
                        "severity": "HIGH",
                        "message": (
                            "Portfolio is experiencing "
                            "a significant drawdown"
                        ),
                    }
                )

            elif drawdown_pct >= Decimal("5"):
                alerts.append(
                    {
                        "alert_type": "DRAWDOWN",
                        "severity": "MEDIUM",
                        "message": (
                            "Portfolio drawdown requires "
                            "monitoring"
                        ),
                    }
                )

        var_99_raw = var_result.get(
            "var_99_pct"
        )

        if var_99_raw is not None:
            var_99 = Decimal(
                str(var_99_raw)
            )

            if var_99 >= Decimal("5"):
                alerts.append(
                    {
                        "alert_type": "TAIL_LOSS",
                        "severity": "HIGH",
                        "message": (
                            "Estimated 99% daily loss "
                            "is materially elevated"
                        ),
                    }
                )

            elif var_99 >= Decimal("3"):
                alerts.append(
                    {
                        "alert_type": "TAIL_LOSS",
                        "severity": "MEDIUM",
                        "message": (
                            "Estimated 99% daily loss "
                            "requires monitoring"
                        ),
                    }
                )

        liquidity_score_raw = liquidity.get(
            "portfolio_liquidity_score"
        )

        if liquidity_score_raw is not None:
            liquidity_score = Decimal(
                str(liquidity_score_raw)
            )

            if liquidity_score < Decimal("20"):
                alerts.append(
                    {
                        "alert_type": "LIQUIDITY",
                        "severity": "CRITICAL",
                        "message": (
                            "Portfolio liquidity is "
                            "severely constrained"
                        ),
                    }
                )

            elif liquidity_score < Decimal("40"):
                alerts.append(
                    {
                        "alert_type": "LIQUIDITY",
                        "severity": "HIGH",
                        "message": (
                            "Portfolio liquidity risk "
                            "is elevated"
                        ),
                    }
                )

        severity_rank = {
            "CRITICAL": 3,
            "HIGH": 2,
            "MEDIUM": 1,
        }

        alerts.sort(
            key=lambda item: severity_rank.get(
                item["severity"],
                0,
            ),
            reverse=True,
        )

        critical_count = sum(
            1
            for alert in alerts
            if alert["severity"] == "CRITICAL"
        )

        high_count = sum(
            1
            for alert in alerts
            if alert["severity"] == "HIGH"
        )

        medium_count = sum(
            1
            for alert in alerts
            if alert["severity"] == "MEDIUM"
        )

        if critical_count > 0:
            alert_status = "Critical"

        elif high_count > 0:
            alert_status = "High"

        elif medium_count > 0:
            alert_status = "Medium"

        else:
            alert_status = "Normal"

        if not alerts:
            alerts.append(
                {
                    "alert_type": "SYSTEM",
                    "severity": "NORMAL",
                    "message": (
                        "No major portfolio risk alerts detected"
                    ),
                }
            )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "alert_status": alert_status,
            "alert_count": len(alerts),
            "critical_alert_count": critical_count,
            "high_alert_count": high_count,
            "medium_alert_count": medium_count,
            "alerts": alerts,
            "message": None,
        }


portfolio_risk_alerts_service = (
    PortfolioRiskAlertsService()
)