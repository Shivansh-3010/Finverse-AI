from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PortfolioCreate(BaseModel):
    user_id: UUID
    name: str = Field(
        min_length=1,
        max_length=255,
    )
    total_value: Decimal = Decimal("0.00")


class PortfolioResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    user_id: UUID
    name: str
    total_value: Decimal
    created_at: datetime
    updated_at: datetime

class PortfolioBetaResponse(BaseModel):
    portfolio_id: UUID
    benchmark: str
    timeframe: str
    lookback_days: int
    beta: Decimal | None = None
    observation_count: int
    portfolio_return_mean: Decimal | None = None
    benchmark_return_mean: Decimal | None = None
    message: str | None = None
    
class PortfolioRiskAdjustedResponse(BaseModel):
    portfolio_id: UUID
    benchmark: str
    timeframe: str
    lookback_days: int
    observation_count: int

    sharpe_ratio: Decimal | None = None
    sortino_ratio: Decimal | None = None
    treynor_ratio: Decimal | None = None
    alpha: Decimal | None = None
    tracking_error: Decimal | None = None

    portfolio_return_mean: Decimal | None = None
    benchmark_return_mean: Decimal | None = None
    beta: Decimal | None = None

    message: str | None = None