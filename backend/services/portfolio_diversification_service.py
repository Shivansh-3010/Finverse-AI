from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from services.portfolio_exposure_service import (
    portfolio_exposure_service,
)
from services.portfolio_correlation_service import (
    portfolio_correlation_service,
)


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioDiversificationService:

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        exposure = (
            portfolio_exposure_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
            )
        )

        correlation = (
            portfolio_correlation_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
                timeframe=timeframe,
                lookback_days=lookback_days,
            )
        )

        exposures = exposure["exposures"]
        position_count = len(exposures)

        base_response = {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
            "position_count": position_count,
        }

        if position_count == 0:
            return {
                **base_response,
                "diversification_score": None,
                "effective_number_of_positions": None,
                "concentration_score": None,
                "average_pairwise_correlation": None,
                "max_pairwise_correlation": None,
                "diversification_category": "Insufficient Data",
                "risk_flags": [
                    "No portfolio positions available"
                ],
                "message": "Portfolio has no active positions",
            }

        weights = []

        for item in exposures:
            weights.append(
                Decimal(
                    str(item["portfolio_weight_pct"])
                ) / Decimal("100")
            )

        weight_squared_sum = sum(
            (
                weight * weight
                for weight in weights
            ),
            Decimal("0"),
        )

        effective_number = (
            Decimal("1") / weight_squared_sum
            if weight_squared_sum > Decimal("0")
            else Decimal("0")
        )

        effective_number = _round(
            effective_number
        )

        concentration_score = _round(
            weight_squared_sum
            * Decimal("100")
        )

        matrix = correlation.get("matrix", {})

        pairwise_correlations = []

        symbols = correlation.get(
            "symbols",
            [],
        )

        for index, symbol_x in enumerate(symbols):

            for symbol_y in symbols[index + 1:]:

                value = (
                    matrix
                    .get(symbol_x, {})
                    .get(symbol_y)
                )

                if value is None:
                    continue

                pairwise_correlations.append(
                    Decimal(str(value))
                )

        if pairwise_correlations:

            average_correlation = (
                sum(
                    pairwise_correlations,
                    Decimal("0"),
                )
                / Decimal(
                    len(pairwise_correlations)
                )
            )

            max_correlation = max(
                pairwise_correlations
            )

            average_correlation = _round(
                average_correlation
            )

            max_correlation = _round(
                max_correlation
            )

        else:

            average_correlation = None
            max_correlation = None

        risk_flags = []

        largest_position = (
            exposure.get("largest_position")
        )

        largest_weight = (
            Decimal(
                str(
                    largest_position[
                        "portfolio_weight_pct"
                    ]
                )
            )
            if largest_position
            else Decimal("0")
        )

        if largest_weight >= Decimal("50"):
            risk_flags.append(
                "Single position exceeds 50% of portfolio"
            )
        elif largest_weight >= Decimal("35"):
            risk_flags.append(
                "High single-position concentration"
            )

        if concentration_score >= Decimal("50"):
            risk_flags.append(
                "High portfolio concentration"
            )
        elif concentration_score >= Decimal("35"):
            risk_flags.append(
                "Moderate portfolio concentration"
            )

        if (
            average_correlation is not None
            and average_correlation >= Decimal("0.75")
        ):
            risk_flags.append(
                "Holdings have high average correlation"
            )
        elif (
            average_correlation is not None
            and average_correlation >= Decimal("0.50")
        ):
            risk_flags.append(
                "Holdings have moderate average correlation"
            )

        if position_count <= 2:
            risk_flags.append(
                "Portfolio contains very few positions"
            )
        elif position_count <= 4:
            risk_flags.append(
                "Portfolio contains a limited number of positions"
            )

        if (
            effective_number >= Decimal("7")
            and concentration_score < Decimal("20")
        ):
            category = "Highly Diversified"

        elif (
            effective_number >= Decimal("4")
            and concentration_score < Decimal("30")
        ):
            category = "Diversified"

        elif (
            effective_number >= Decimal("2")
            and concentration_score < Decimal("50")
        ):
            category = "Moderately Diversified"

        else:
            category = "Concentrated"

        if average_correlation is not None:

            if average_correlation >= Decimal("0.75"):
                category = "Highly Correlated"

            elif (
                average_correlation >= Decimal("0.50")
                and category
                in {
                    "Highly Diversified",
                    "Diversified",
                }
            ):
                category = "Moderately Correlated"

        if not risk_flags:
            risk_flags.append(
                "No major diversification risks detected"
            )

        # ---------------------------------------------------------
        # Diversification score
        #
        # 40% concentration
        # 30% position breadth
        # 30% correlation
        # ---------------------------------------------------------

        concentration_component = max(
            Decimal("0"),
            min(
                Decimal("100"),
                (
                    Decimal("1")
                    - weight_squared_sum
                )
                * Decimal("100"),
            ),
        )

        if position_count <= 0:
            breadth_component = Decimal("0")

        else:
            breadth_component = min(
                Decimal("100"),
                effective_number
                / Decimal("10")
                * Decimal("100"),
            )

        if average_correlation is None:
            correlation_component = Decimal("50")

        else:
            correlation_component = (
                Decimal("1")
                - (
                    (
                        average_correlation
                        + Decimal("1")
                    )
                    / Decimal("2")
                )
            ) * Decimal("100")

            correlation_component = max(
                Decimal("0"),
                min(
                    Decimal("100"),
                    correlation_component,
                ),
            )

        diversification_score = (
            concentration_component
            * Decimal("0.40")
            + breadth_component
            * Decimal("0.30")
            + correlation_component
            * Decimal("0.30")
        )

        diversification_score = max(
            Decimal("0"),
            min(
                Decimal("100"),
                diversification_score,
            ),
        )

        return {
            **base_response,
            "diversification_score": _round(
                diversification_score
            ),
            "effective_number_of_positions":
                effective_number,
            "concentration_score":
                concentration_score,
            "average_pairwise_correlation":
                average_correlation,
            "max_pairwise_correlation":
                max_correlation,
            "diversification_category":
                category,
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_diversification_service = (
    PortfolioDiversificationService()
)