
from datetime import date
from decimal import Decimal, ROUND_HALF_UP


MONEY = Decimal("0.01")
ZERO = Decimal("0")


class PortfolioGoalService:
    """Calculate progress and projections for portfolio goals."""

    @staticmethod
    def _money(value: Decimal) -> Decimal:
        return value.quantize(MONEY, rounding=ROUND_HALF_UP)

    @staticmethod
    def _validate_inputs(
        current_amount: Decimal,
        target_amount: Decimal,
        monthly_contribution: Decimal,
        annual_return_pct: Decimal,
        months: int,
    ) -> None:
        if current_amount < ZERO:
            raise ValueError("Current amount cannot be negative")
        if target_amount <= ZERO:
            raise ValueError("Target amount must be greater than zero")
        if monthly_contribution < ZERO:
            raise ValueError("Monthly contribution cannot be negative")
        if annual_return_pct <= Decimal("-100"):
            raise ValueError("Annual return must be greater than -100%")
        if months <= 0:
            raise ValueError("Months must be greater than zero")

    @staticmethod
    def months_until(target_date: date, today: date | None = None) -> int:
        today = today or date.today()

        if target_date <= today:
            raise ValueError("Target date must be in the future")

        months = (
            (target_date.year - today.year) * 12
            + target_date.month
            - today.month
        )

        if target_date.day > today.day:
            months += 1

        return max(months, 1)

    @classmethod
    def project(
        cls,
        current_amount: Decimal,
        target_amount: Decimal,
        monthly_contribution: Decimal,
        annual_return_pct: Decimal,
        months: int,
    ) -> dict:
        cls._validate_inputs(
            current_amount,
            target_amount,
            monthly_contribution,
            annual_return_pct,
            months,
        )

        monthly_rate = (
            Decimal("1") + annual_return_pct / Decimal("100")
        ) ** (Decimal("1") / Decimal("12")) - Decimal("1")

        if monthly_rate == ZERO:
            projected_value = (
                current_amount + monthly_contribution * months
            )
        else:
            growth = (Decimal("1") + monthly_rate) ** months
            contribution_factor = (growth - Decimal("1")) / monthly_rate
            projected_value = (
                current_amount * growth
                + monthly_contribution * contribution_factor
            )

        remaining = max(target_amount - current_amount, ZERO)
        progress_pct = min(
            current_amount / target_amount * Decimal("100"),
            Decimal("100"),
        )

        return {
            "months": months,
            "current_amount": cls._money(current_amount),
            "target_amount": cls._money(target_amount),
            "projected_value": cls._money(projected_value),
            "remaining_amount": cls._money(remaining),
            "progress_pct": cls._money(progress_pct),
            "goal_reached_in_projection": projected_value >= target_amount,
            "assumed_annual_return_pct": annual_return_pct,
            "disclaimer": (
                "Projection is illustrative, assumes a constant annual "
                "return and end-of-month contributions, and is not a "
                "guarantee of investment performance."
            ),
        }

    @classmethod
    def required_monthly_contribution(
        cls,
        current_amount: Decimal,
        target_amount: Decimal,
        annual_return_pct: Decimal,
        months: int,
    ) -> Decimal:
        cls._validate_inputs(
            current_amount=current_amount,
            target_amount=target_amount,
            monthly_contribution=ZERO,
            annual_return_pct=annual_return_pct,
            months=months,
        )

        monthly_rate = (
            Decimal("1") + annual_return_pct / Decimal("100")
        ) ** (Decimal("1") / Decimal("12")) - Decimal("1")

        if monthly_rate == ZERO:
            contribution = (
                target_amount - current_amount
            ) / Decimal(months)
        else:
            growth = (Decimal("1") + monthly_rate) ** months
            future_current = current_amount * growth
            contribution_factor = (
                growth - Decimal("1")
            ) / monthly_rate

            contribution = (
                target_amount - future_current
            ) / contribution_factor

        return cls._money(max(contribution, ZERO))


portfolio_goal_service = PortfolioGoalService()
