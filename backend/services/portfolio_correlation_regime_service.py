from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_correlation_service import (
    portfolio_correlation_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioCorrelationRegimeService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
    ) -> dict:

        correlation = (
            portfolio_correlation_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        average_correlation_raw = correlation.get(
            "average_correlation"
        )

        if average_correlation_raw is None:
            return {
                "portfolio_id": portfolio_id,
                "timeframe": timeframe,
                "average_correlation": None,
                "correlation_regime": "Insufficient Data",
                "diversification_quality": "Insufficient Data",
                "risk_implication": "Insufficient correlation data",
                "message": "Insufficient correlation history",
            }

        average_correlation = Decimal(
            str(average_correlation_raw)
        )

        if average_correlation >= Decimal("0.80"):
            regime = "Highly Correlated"
            diversification_quality = "Very Weak"
            risk_implication = (
                "Portfolio holdings may amplify common market movements"
            )

        elif average_correlation >= Decimal("0.60"):
            regime = "Highly Correlated"
            diversification_quality = "Weak"
            risk_implication = (
                "Portfolio has elevated common-factor exposure"
            )

        elif average_correlation >= Decimal("0.40"):
            regime = "Moderately Correlated"
            diversification_quality = "Moderate"
            risk_implication = (
                "Holdings provide partial diversification"
            )

        elif average_correlation >= Decimal("0.20"):
            regime = "Low Correlation"
            diversification_quality = "Good"
            risk_implication = (
                "Portfolio benefits from relatively independent holdings"
            )

        else:
            regime = "Very Low Correlation"
            diversification_quality = "Strong"
            risk_implication = (
                "Holdings provide strong diversification benefits"
            )

        return {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "average_correlation": _round(
                average_correlation
            ),
            "correlation_regime": regime,
            "diversification_quality": diversification_quality,
            "risk_implication": risk_implication,
            "message": None,
        }


portfolio_correlation_regime_service = (
    PortfolioCorrelationRegimeService()
)