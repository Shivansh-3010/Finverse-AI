
from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from models.portfolio_goal import PortfolioGoal
from services.portfolio_goal_crud_service import (
    PortfolioGoalCRUDService,
)


@pytest.fixture
def service():
    return PortfolioGoalCRUDService()


@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def portfolio():
    portfolio = MagicMock()
    portfolio.id = uuid4()
    return portfolio


@pytest.fixture
def goal(portfolio):
    goal = MagicMock(spec=PortfolioGoal)
    goal.id = uuid4()
    goal.portfolio_id = portfolio.id
    goal.target_date = date.today() + timedelta(days=365)
    return goal


def test_create_goal_persists_and_returns_goal(
    service, db, portfolio
):
    db.query.return_value.filter.return_value.first.return_value = (
        portfolio
    )
    payload = {
        "name": "Emergency Fund",
        "goal_type": "savings",
        "target_amount": Decimal("100000.00"),
        "current_amount": Decimal("10000.00"),
        "monthly_contribution": Decimal("5000.00"),
        "target_date": date.today() + timedelta(days=365),
        "expected_annual_return_pct": Decimal("5.000"),
    }

    result = service.create(db, portfolio.id, payload)

    assert isinstance(result, PortfolioGoal)
    assert result.name == "Emergency Fund"
    assert result.portfolio_id == portfolio.id
    db.add.assert_called_once_with(result)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(result)


def test_create_goal_rejects_missing_portfolio(service, db):
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(LookupError, match="Portfolio not found"):
        service.create(
            db,
            uuid4(),
            {
                "name": "Test",
                "goal_type": "savings",
                "target_amount": Decimal("1000"),
                "current_amount": Decimal("0"),
                "monthly_contribution": Decimal("0"),
                "target_date": date.today() + timedelta(days=365),
                "expected_annual_return_pct": Decimal("5"),
            },
        )

    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_create_goal_rejects_past_target_date(
    service, db, portfolio
):
    db.query.return_value.filter.return_value.first.return_value = (
        portfolio
    )

    with pytest.raises(ValueError, match="future"):
        service.create(
            db,
            portfolio.id,
            {
                "name": "Expired Goal",
                "goal_type": "savings",
                "target_amount": Decimal("1000"),
                "current_amount": Decimal("0"),
                "monthly_contribution": Decimal("0"),
                "target_date": date.today(),
                "expected_annual_return_pct": Decimal("5"),
            },
        )

    db.add.assert_not_called()


def test_update_goal_applies_changes(
    service, db, portfolio, goal
):
    db.query.return_value.filter.return_value.first.return_value = goal
    new_name = "Updated Emergency Fund"

    result = service.update(
        db,
        portfolio.id,
        goal.id,
        {"name": new_name},
    )

    assert result is goal
    assert goal.name == new_name
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(goal)


def test_delete_goal_commits_deletion(
    service, db, portfolio, goal
):
    db.query.return_value.filter.return_value.first.return_value = goal

    result = service.delete(db, portfolio.id, goal.id)

    assert result is True
    db.delete.assert_called_once_with(goal)
    db.commit.assert_called_once()


def test_delete_missing_goal_returns_false(service, db):
    db.query.return_value.filter.return_value.first.return_value = None

    result = service.delete(db, uuid4(), uuid4())

    assert result is False
    db.delete.assert_not_called()
    db.commit.assert_not_called()
