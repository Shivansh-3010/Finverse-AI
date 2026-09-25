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
    
class PortfolioAttributionPositionResponse(BaseModel):
    symbol: str
    quantity: Decimal
    cost_basis: Decimal
    portfolio_weight_pct: Decimal
    start_price: Decimal | None = None
    end_price: Decimal | None = None
    return_pct: Decimal | None = None
    pnl: Decimal | None = None
    return_contribution_pct: Decimal | None = None
    message: str | None = None


class PortfolioAttributionResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int
    position_count: int
    total_cost_basis: Decimal
    portfolio_return: Decimal | None = None
    total_pnl_contribution: Decimal
    positions: list[PortfolioAttributionPositionResponse]
    message: str | None = None
    
class PortfolioExposurePositionResponse(BaseModel):
    symbol: str
    market_value: Decimal
    portfolio_weight_pct: Decimal
    unrealized_pnl: Decimal
    unrealized_return_pct: Decimal


class PortfolioExposureResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    position_count: int
    total_market_value: Decimal
    largest_position: PortfolioExposurePositionResponse | None = None
    herfindahl_index: Decimal
    exposures: list[PortfolioExposurePositionResponse]
    message: str | None = None