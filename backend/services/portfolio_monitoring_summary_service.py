from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_risk_score_service import (
    portfolio_risk_score_service,
)
from services.portfolio_health_score_service import (
    portfolio_health_score_service,
)
from services.portfolio_risk_alerts_service import (
    portfolio_risk_alerts_service,
)
from services.portfolio_drawdown_service import (
    portfolio_drawdown_service,
)
from services.portfolio_liquidity_service import (
    portfolio_liquidity_service,
)
from services.portfolio_var_service import (
    portfolio_var_service,
)


class PortfolioMonitoringSummaryService:

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

        health = (
            portfolio_health_score_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        alerts = (
            portfolio_risk_alerts_service.calculate(
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

        liquidity = (
            portfolio_liquidity_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
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

        overall_risk_score = risk_score.get(
            "overall_risk_score"
        )

        health_score = health.get(
            "health_score"
        )

        current_drawdown = drawdown.get(
            "current_drawdown_pct"
        )

        liquidity_score = liquidity.get(
            "portfolio_liquidity_score"
        )

        var_95 = var_result.get(
            "var_95_pct"
        )

        var_99 = var_result.get(
            "var_99_pct"
        )

        if overall_risk_score is None:
            monitoring_status = "Insufficient Data"

        else:
            risk_value = Decimal(
                str(overall_risk_score)
            )

            if risk_value >= Decimal("80"):
                monitoring_status = "Critical"

            elif risk_value >= Decimal("60"):
                monitoring_status = "High Risk"

            elif risk_value >= Decimal("40"):
                monitoring_status = "Moderate Risk"

            else:
                monitoring_status = "Normal"

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "monitoring_status": monitoring_status,
            "overall_risk_score": overall_risk_score,
            "health_score": health_score,
            "current_drawdown_pct": current_drawdown,
            "liquidity_score": liquidity_score,
            "var_95_pct": var_95,
            "var_99_pct": var_99,
            "risk_alert_status": alerts.get(
                "alert_status"
            ),
            "risk_alert_count": alerts.get(
                "alert_count",
                0,
            ),
            "critical_alert_count": alerts.get(
                "critical_alert_count",
                0,
            ),
            "high_alert_count": alerts.get(
                "high_alert_count",
                0,
            ),
            "medium_alert_count": alerts.get(
                "medium_alert_count",
                0,
            ),
            "risk_category": risk_score.get(
                "risk_category"
            ),
            "health_category": health.get(
                "health_category"
            ),
            "drawdown_category": drawdown.get(
                "drawdown_category"
            ),
            "liquidity_category": liquidity.get(
                "liquidity_category"
            ),
            "alerts": alerts.get(
                "alerts",
                [],
            ),
            "risk_flags": (
                risk_score.get(
                    "risk_flags",
                    [],
                )
                + health.get(
                    "risk_flags",
                    [],
                )
                + drawdown.get(
                    "risk_flags",
                    [],
                )
            ),
            "message": None,
        }


portfolio_monitoring_summary_service = (
    PortfolioMonitoringSummaryService()
)