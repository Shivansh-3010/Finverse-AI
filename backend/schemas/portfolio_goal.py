
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PortfolioGoalCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    goal_type: str = Field(min_length=1, max_length=50)
    target_amount: Decimal = Field(gt=0, max_digits=15, decimal_places=2)
    current_amount: Decimal = Field(
        default=Decimal("0.00"), ge=0, max_digits=15, decimal_places=2
    )
    monthly_contribution: Decimal = Field(
        default=Decimal("0.00"), ge=0, max_digits=15, decimal_places=2
    )
    target_date: date
    expected_annual_return_pct: Decimal = Field(
        default=Decimal("7.000"), gt=-100, le=100,
        max_digits=6, decimal_places=3,
    )


class PortfolioGoalUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    goal_type: str | None = Field(default=None, min_length=1, max_length=50)
    target_amount: Decimal | None = Field(
        default=None, gt=0, max_digits=15, decimal_places=2
    )
    current_amount: Decimal | None = Field(
        default=None, ge=0, max_digits=15, decimal_places=2
    )
    monthly_contribution: Decimal | None = Field(
        default=None, ge=0, max_digits=15, decimal_places=2
    )
    target_date: date | None = None
    expected_annual_return_pct: Decimal | None = Field(
        default=None, gt=-100, le=100,
        max_digits=6, decimal_places=3,
    )


class PortfolioGoalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    portfolio_id: UUID
    name: str
    goal_type: str
    target_amount: Decimal
    current_amount: Decimal
    monthly_contribution: Decimal
    target_date: date
    expected_annual_return_pct: Decimal
    created_at: datetime
    updated_at: datetime
