from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_risk_score_service import (
    portfolio_risk_score_service,
)
from services.portfolio_diversification_service import (
    portfolio_diversification_service,
)
from services.portfolio_liquidity_service import (
    portfolio_liquidity_service,
)
from services.portfolio_drawdown_service import (
    portfolio_drawdown_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioHealthScoreService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        risk = portfolio_risk_score_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
            lookback_days=lookback_days,
        )

        diversification = (
            portfolio_diversification_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        liquidity = (
            portfolio_liquidity_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
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

        risk_score_raw = risk.get(
            "overall_risk_score"
        )

        diversification_score_raw = (
            diversification.get(
                "diversification_score"
            )
        )

        liquidity_score_raw = liquidity.get(
            "portfolio_liquidity_score"
        )

        drawdown_raw = drawdown.get(
            "current_drawdown_pct"
        )

        if risk_score_raw is None:
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "health_score": None,
                "health_category": "Insufficient Data",
                "component_scores": {},
                "risk_flags": [],
                "message": "Insufficient portfolio health data",
            }

        risk_score = Decimal(
            str(risk_score_raw)
        )

        # Risk score is higher = worse.
        risk_health = Decimal("100") - risk_score

        if diversification_score_raw is not None:
            diversification_health = Decimal(
                str(diversification_score_raw)
            )
        else:
            diversification_health = Decimal("50")

        if liquidity_score_raw is not None:
            liquidity_health = Decimal(
                str(liquidity_score_raw)
            )
        else:
            liquidity_health = Decimal("50")

        if drawdown_raw is not None:
            drawdown_pct = abs(
                Decimal(str(drawdown_raw))
            )

            drawdown_health = max(
                Decimal("0"),
                Decimal("100")
                - (
                    drawdown_pct
                    * Decimal("4")
                ),
            )
        else:
            drawdown_health = Decimal("50")

        health_score = (
            risk_health * Decimal("0.35")
            + diversification_health * Decimal("0.25")
            + liquidity_health * Decimal("0.20")
            + drawdown_health * Decimal("0.20")
        )

        health_score = max(
            Decimal("0"),
            min(
                Decimal("100"),
                health_score,
            ),
        )

        if health_score >= Decimal("80"):
            health_category = "Excellent"

        elif health_score >= Decimal("65"):
            health_category = "Healthy"

        elif health_score >= Decimal("50"):
            health_category = "Needs Attention"

        elif health_score >= Decimal("35"):
            health_category = "Weak"

        else:
            health_category = "Critical"

        risk_flags = []

        if risk_score >= Decimal("60"):
            risk_flags.append(
                "Overall portfolio risk is elevated"
            )

        if (
            diversification_score_raw is not None
            and Decimal(
                str(diversification_score_raw)
            ) < Decimal("40")
        ):
            risk_flags.append(
                "Portfolio diversification is weak"
            )

        if (
            liquidity_score_raw is not None
            and Decimal(
                str(liquidity_score_raw)
            ) < Decimal("40")
        ):
            risk_flags.append(
                "Portfolio liquidity is weak"
            )

        if (
            drawdown_raw is not None
            and abs(
                Decimal(str(drawdown_raw))
            ) >= Decimal("10")
        ):
            risk_flags.append(
                "Portfolio is experiencing a significant drawdown"
            )

        if not risk_flags:
            risk_flags.append(
                "No major portfolio health concerns detected"
            )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "health_score": _round(
                health_score
            ),
            "health_category": health_category,
            "component_scores": {
                "risk_health": _round(
                    risk_health
                ),
                "diversification_health": _round(
                    diversification_health
                ),
                "liquidity_health": _round(
                    liquidity_health
                ),
                "drawdown_health": _round(
                    drawdown_health
                ),
            },
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_health_score_service = (
    PortfolioHealthScoreService()
)