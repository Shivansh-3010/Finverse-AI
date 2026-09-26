from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_diversification_service import (
    portfolio_diversification_service,
)
from services.portfolio_factor_exposure_service import (
    portfolio_factor_exposure_service,
)
from services.portfolio_stress_test_service import (
    portfolio_stress_test_service,
)
from services.portfolio_liquidity_service import (
    portfolio_liquidity_service,
)
from services.portfolio_risk_adjusted_service import (
    portfolio_risk_adjusted_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioRiskScoreService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        benchmark: str = "NIFTY50",
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        diversification = (
            portfolio_diversification_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        factor_exposure = (
            portfolio_factor_exposure_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        stress_test = (
            portfolio_stress_test_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                scenario="market_shock",
                shock_pct=Decimal("-10"),
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

        risk_adjusted = (
            portfolio_risk_adjusted_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                benchmark=benchmark,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        risk_components = {}
        risk_flags = []

        # ---------------------------------------------------------
        # 1. Concentration Risk
        # ---------------------------------------------------------

        concentration = diversification.get(
            "concentration_score"
        )

        if concentration is not None:
            concentration = Decimal(str(concentration))

            if concentration >= Decimal("50"):
                concentration_risk = Decimal("100")
            elif concentration >= Decimal("35"):
                concentration_risk = Decimal("75")
            elif concentration >= Decimal("20"):
                concentration_risk = Decimal("50")
            else:
                concentration_risk = Decimal("20")

            risk_components["concentration_risk"] = (
                _round(concentration_risk)
            )

        # ---------------------------------------------------------
        # 2. Correlation Risk
        # ---------------------------------------------------------

        correlation = diversification.get(
            "average_pairwise_correlation"
        )

        if correlation is not None:
            correlation = Decimal(str(correlation))

            if correlation >= Decimal("0.75"):
                correlation_risk = Decimal("100")
            elif correlation >= Decimal("0.50"):
                correlation_risk = Decimal("70")
            elif correlation >= Decimal("0.25"):
                correlation_risk = Decimal("40")
            else:
                correlation_risk = Decimal("15")

            risk_components["correlation_risk"] = (
                _round(correlation_risk)
            )

        # ---------------------------------------------------------
        # 3. Volatility Risk
        # ---------------------------------------------------------

        volatility = factor_exposure.get(
            "portfolio_factor_exposure",
            {},
        ).get(
            "realized_volatility_pct"
        )

        if volatility is not None:
            volatility = Decimal(str(volatility))

            if volatility >= Decimal("40"):
                volatility_risk = Decimal("100")
            elif volatility >= Decimal("30"):
                volatility_risk = Decimal("80")
            elif volatility >= Decimal("20"):
                volatility_risk = Decimal("60")
            elif volatility >= Decimal("10"):
                volatility_risk = Decimal("35")
            else:
                volatility_risk = Decimal("15")

            risk_components["volatility_risk"] = (
                _round(volatility_risk)
            )

        # ---------------------------------------------------------
        # 4. Liquidity Risk
        # ---------------------------------------------------------

        liquidity_score = liquidity.get(
            "portfolio_liquidity_score"
        )

        if liquidity_score is not None:
            liquidity_score = Decimal(
                str(liquidity_score)
            )

            liquidity_risk = (
                Decimal("100") - liquidity_score
            )

            risk_components["liquidity_risk"] = (
                _round(liquidity_risk)
            )

        # ---------------------------------------------------------
        # 5. Stress Risk
        # ---------------------------------------------------------

        stress_return = stress_test.get(
            "estimated_return_impact_pct"
        )

        if stress_return is not None:
            stress_return = abs(
                Decimal(str(stress_return))
            )

            if stress_return >= Decimal("15"):
                stress_risk = Decimal("100")
            elif stress_return >= Decimal("10"):
                stress_risk = Decimal("80")
            elif stress_return >= Decimal("5"):
                stress_risk = Decimal("60")
            else:
                stress_risk = Decimal("30")

            risk_components["stress_risk"] = (
                _round(stress_risk)
            )

        # ---------------------------------------------------------
        # 6. Market / Beta Risk
        # ---------------------------------------------------------

        beta = factor_exposure.get(
            "portfolio_factor_exposure",
            {},
        ).get("market_beta")

        if beta is not None:
            beta = abs(Decimal(str(beta)))

            if beta >= Decimal("1.50"):
                beta_risk = Decimal("100")
            elif beta >= Decimal("1.20"):
                beta_risk = Decimal("80")
            elif beta >= Decimal("1.00"):
                beta_risk = Decimal("60")
            elif beta >= Decimal("0.75"):
                beta_risk = Decimal("40")
            else:
                beta_risk = Decimal("20")

            risk_components["market_beta_risk"] = (
                _round(beta_risk)
            )

        # ---------------------------------------------------------
        # Composite Score
        # ---------------------------------------------------------

        weights = {
            "concentration_risk": Decimal("0.20"),
            "correlation_risk": Decimal("0.15"),
            "volatility_risk": Decimal("0.20"),
            "liquidity_risk": Decimal("0.10"),
            "stress_risk": Decimal("0.20"),
            "market_beta_risk": Decimal("0.15"),
        }

        weighted_score = Decimal("0")
        total_weight = Decimal("0")

        for component, weight in weights.items():

            value = risk_components.get(component)

            if value is None:
                continue

            weighted_score += value * weight
            total_weight += weight

        if total_weight > Decimal("0"):
            overall_risk_score = (
                weighted_score / total_weight
            )
        else:
            overall_risk_score = None

        if overall_risk_score is None:
            risk_category = "Insufficient Data"

        elif overall_risk_score >= Decimal("75"):
            risk_category = "Very High Risk"

        elif overall_risk_score >= Decimal("60"):
            risk_category = "High Risk"

        elif overall_risk_score >= Decimal("40"):
            risk_category = "Moderate Risk"

        elif overall_risk_score >= Decimal("20"):
            risk_category = "Low Risk"

        else:
            risk_category = "Very Low Risk"

        # ---------------------------------------------------------
        # Risk Flags
        # ---------------------------------------------------------

        risk_flags.extend(
            diversification.get(
                "risk_flags",
                [],
            )
        )

        risk_flags.extend(
            factor_exposure.get(
                "risk_flags",
                [],
            )
        )

        risk_flags.extend(
            stress_test.get(
                "risk_flags",
                [],
            )
        )

        risk_flags.extend(
            liquidity.get(
                "risk_flags",
                [],
            )
        )

        # Remove duplicates while preserving order
        risk_flags = list(
            dict.fromkeys(risk_flags)
        )

        return {
            "portfolio_id": portfolio_id,
            "benchmark": benchmark,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "overall_risk_score": (
                _round(overall_risk_score)
                if overall_risk_score is not None
                else None
            ),
            "risk_category": risk_category,
            "risk_components": risk_components,
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_risk_score_service = (
    PortfolioRiskScoreService()
)