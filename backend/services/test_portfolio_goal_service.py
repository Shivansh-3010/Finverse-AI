
from datetime import date
from decimal import Decimal

import pytest

from services.portfolio_goal_service import PortfolioGoalService


def test_projection_with_zero_return():
    result = PortfolioGoalService.project(
        current_amount=Decimal("1000"),
        target_amount=Decimal("2000"),
        monthly_contribution=Decimal("100"),
        annual_return_pct=Decimal("0"),
        months=10,
    )

    assert result["projected_value"] == Decimal("2000.00")
    assert result["goal_reached_in_projection"] is True


def test_projection_with_positive_return():
    result = PortfolioGoalService.project(
        current_amount=Decimal("1000"),
        target_amount=Decimal("2000"),
        monthly_contribution=Decimal("100"),
        annual_return_pct=Decimal("7"),
        months=12,
    )

    assert result["projected_value"] > Decimal("2200")
    assert result["progress_pct"] == Decimal("50.00")


def test_required_monthly_contribution():
    contribution = PortfolioGoalService.required_monthly_contribution(
        current_amount=Decimal("1000"),
        target_amount=Decimal("2200"),
        annual_return_pct=Decimal("0"),
        months=12,
    )

    assert contribution == Decimal("100.00")


def test_negative_contribution_rejected():
    with pytest.raises(ValueError, match="cannot be negative"):
        PortfolioGoalService.project(
            current_amount=Decimal("100"),
            target_amount=Decimal("1000"),
            monthly_contribution=Decimal("-10"),
            annual_return_pct=Decimal("5"),
            months=12,
        )


def test_past_target_date_rejected():
    with pytest.raises(ValueError, match="future"):
        PortfolioGoalService.months_until(
            target_date=date(2020, 1, 1),
            today=date(2026, 1, 1),
        )
