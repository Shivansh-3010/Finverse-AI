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

class PortfolioCorrelationResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int
    symbols: list[str]
    observation_count: int
    matrix: dict[str, dict[str, Decimal | None]]
    message: str | None = None

class PortfolioDiversificationResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int
    position_count: int

    diversification_score: Decimal | None = None
    effective_number_of_positions: Decimal | None = None
    concentration_score: Decimal | None = None

    average_pairwise_correlation: Decimal | None = None
    max_pairwise_correlation: Decimal | None = None

    diversification_category: str
    risk_flags: list[str] = []

    message: str | None = None
    
class PortfolioFactorExposurePositionResponse(BaseModel):
    symbol: str
    portfolio_weight_pct: Decimal
    market_beta: Decimal | None = None
    momentum_pct: Decimal | None = None
    realized_volatility_pct: Decimal | None = None
    average_daily_traded_value: Decimal | None = None


class PortfolioFactorExposureSummaryResponse(BaseModel):
    market_beta: Decimal | None = None
    momentum_pct: Decimal | None = None
    realized_volatility_pct: Decimal | None = None


class PortfolioFactorExposureResponse(BaseModel):
    portfolio_id: UUID
    benchmark: str
    timeframe: str
    position_count: int

    portfolio_factor_exposure: (
        PortfolioFactorExposureSummaryResponse | None
    ) = None

    positions: list[
        PortfolioFactorExposurePositionResponse
    ] = []

    risk_flags: list[str] = []

    message: str | None = None
    
class PortfolioStressTestPositionResponse(BaseModel):
    symbol: str
    market_value: Decimal
    portfolio_weight_pct: Decimal
    applied_shock_pct: Decimal
    estimated_pnl_impact: Decimal
    estimated_return_impact_pct: Decimal


class PortfolioStressTestResponse(BaseModel):
    portfolio_id: UUID
    scenario: str
    shock_pct: Decimal
    symbol: str | None = None
    timeframe: str
    position_count: int
    total_market_value: Decimal

    estimated_pnl_impact: Decimal | None = None
    estimated_return_impact_pct: Decimal | None = None
    stressed_portfolio_value: Decimal | None = None

    position_impacts: list[
        PortfolioStressTestPositionResponse
    ]

    risk_flags: list[str]
    message: str | None = None