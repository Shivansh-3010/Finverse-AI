from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import List, Optional

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
    
class PortfolioLiquidityPositionResponse(BaseModel):
    symbol: str
    market_value: Decimal
    portfolio_weight_pct: Decimal
    average_daily_traded_value: Decimal
    daily_turnover_pct: Decimal
    estimated_days_to_liquidate: Decimal | None = None
    liquidity_score: Decimal


class PortfolioLiquidityResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    position_count: int
    total_market_value: Decimal

    portfolio_liquidity_score: Decimal | None = None
    liquidity_category: str
    estimated_daily_turnover_pct: Decimal | None = None

    positions: list[
        PortfolioLiquidityPositionResponse
    ]

    risk_flags: list[str]
    message: str | None = None
    
class PortfolioRiskScoreResponse(BaseModel):
    portfolio_id: UUID
    benchmark: str
    timeframe: str
    lookback_days: int

    overall_risk_score: Decimal | None = None
    risk_category: str

    risk_components: dict[str, Decimal]
    risk_flags: list[str] = []

    message: str | None = None
    
class PortfolioDrawdownResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int
    observation_count: int

    current_portfolio_value: Decimal | None = None
    peak_portfolio_value: Decimal | None = None

    current_drawdown_pct: Decimal | None = None
    maximum_drawdown_pct: Decimal | None = None

    drawdown_duration_days: int | None = None

    recovery_status: str
    recovery_time_days: int | None = None

    drawdown_category: str
    risk_flags: list[str] = []

    message: str | None = None

class PortfolioVaRResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int
    observation_count: int

    var_95_pct: Decimal | None = None
    var_99_pct: Decimal | None = None

    var_95_value: Decimal | None = None
    var_99_value: Decimal | None = None

    expected_shortfall_95_pct: Decimal | None = None
    expected_shortfall_99_pct: Decimal | None = None

    expected_shortfall_95_value: Decimal | None = None
    expected_shortfall_99_value: Decimal | None = None

    worst_historical_return_pct: Decimal | None = None

    risk_category: str
    risk_flags: list[str] = []

    message: str | None = None
    
class PortfolioScenarioAnalysisResponse(BaseModel):
    portfolio_id: UUID
    scenario: str
    timeframe: str
    position_count: int

    total_market_value: Decimal
    estimated_pnl_impact: Decimal
    estimated_return_impact_pct: Decimal
    stressed_portfolio_value: Decimal

    position_impacts: list[dict]
    worst_affected_position: str | None = None

    scenario_category: str
    risk_flags: list[str] = []

    message: str | None = None
    
class PortfolioOptimizationPositionResponse(BaseModel):
    symbol: str
    current_weight_pct: Decimal
    target_weight_pct: Decimal
    weight_change_pct: Decimal
    market_value: Decimal


class PortfolioOptimizationResponse(BaseModel):
    portfolio_id: UUID
    benchmark: str
    timeframe: str
    lookback_days: int
    position_count: int

    current_concentration_score: Decimal | None = None
    optimized_concentration_score: Decimal | None = None
    expected_risk_reduction_pct: Decimal | None = None

    optimization_category: str
    positions: list[PortfolioOptimizationPositionResponse]

    risk_flags: list[str] = []
    message: str | None = None


class PortfolioPerformanceAttributionResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int
    position_count: int

    total_cost_basis: Decimal
    portfolio_return: Decimal | None = None
    total_pnl_contribution: Decimal

    positions: list[PortfolioAttributionPositionResponse]

    message: str | None = None


class PortfolioIntelligenceResponse(BaseModel):
    portfolio_id: UUID
    benchmark: str
    timeframe: str
    lookback_days: int

    intelligence_category: str
    overall_risk_score: Decimal | None = None
    risk_category: str | None = None

    portfolio_summary: dict
    risk: dict
    portfolio_structure: dict

    risk_flags: list[str] = []
    message: str | None = None
    
class PortfolioBenchmarkComparisonResponse(BaseModel):
    portfolio_id: UUID
    benchmark: str
    timeframe: str
    lookback_days: int
    portfolio_return_pct: Optional[Decimal] = None
    benchmark_return_pct: Optional[Decimal] = None
    excess_return_pct: Optional[Decimal] = None
    relative_performance: str
    message: Optional[str] = None


class PortfolioAlphaBetaResponse(BaseModel):
    portfolio_id: UUID
    benchmark: str
    timeframe: str
    lookback_days: int
    alpha_pct: Optional[Decimal] = None
    beta: Optional[Decimal] = None
    portfolio_return_pct: Optional[Decimal] = None
    benchmark_return_pct: Optional[Decimal] = None
    risk_characterization: str
    message: Optional[str] = None


class PortfolioRiskAdjustedReturnResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int
    portfolio_return_pct: Optional[Decimal] = None
    risk_free_rate_pct: Optional[Decimal] = None
    downside_risk_pct: Optional[Decimal] = None
    risk_adjusted_return: Optional[Decimal] = None
    performance_category: str
    message: Optional[str] = None


class PortfolioRiskDecompositionResponse(BaseModel):
    portfolio_id: UUID
    benchmark: str
    timeframe: str
    lookback_days: int
    overall_risk_score: Optional[Decimal] = None
    dominant_risk: Optional[str] = None
    risk_components: dict
    risk_contributions_pct: dict
    risk_level: str
    message: Optional[str] = None


class PortfolioRebalancingPositionResponse(BaseModel):
    symbol: str
    current_weight_pct: Decimal
    target_weight_pct: Decimal
    weight_change_pct: Decimal
    action: str
    priority: str


class PortfolioRebalancingResponse(BaseModel):
    portfolio_id: UUID
    benchmark: str
    timeframe: str
    lookback_days: int
    position_count: int
    estimated_turnover_pct: Optional[Decimal] = None
    rebalancing_required: bool
    positions: list[PortfolioRebalancingPositionResponse]
    message: Optional[str] = None


class PortfolioRecommendationItemResponse(BaseModel):
    action: str
    priority: str
    reason: str


class PortfolioRecommendationResponse(BaseModel):
    portfolio_id: UUID
    benchmark: str
    timeframe: str
    lookback_days: int
    recommendation_count: int
    recommendations: list[
        PortfolioRecommendationItemResponse
    ]
    risk_category: Optional[str] = None
    diversification_category: Optional[str] = None
    liquidity_category: Optional[str] = None
    rebalancing_required: bool
    message: Optional[str] = None
    
class PortfolioExposureAttributionResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str

    position_count: int
    total_market_value: Optional[Decimal] = None

    positive_exposure_pct: Optional[Decimal] = None
    negative_exposure_pct: Optional[Decimal] = None
    net_exposure_pct: Optional[Decimal] = None

    largest_exposure_symbol: Optional[str] = None
    largest_exposure_pct: Optional[Decimal] = None

    positions: list[dict] = Field(default_factory=list)

    message: Optional[str] = None


class PortfolioVolatilityForecastResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int

    current_volatility_pct: Optional[Decimal] = None
    forecast_volatility_pct: Optional[Decimal] = None

    volatility_change_pct: Optional[Decimal] = None
    volatility_category: Optional[str] = None

    risk_flags: list[str] = Field(default_factory=list)

    message: Optional[str] = None


class PortfolioCorrelationRegimeResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str

    average_correlation: Optional[Decimal] = None

    correlation_regime: Optional[str] = None
    diversification_quality: Optional[str] = None
    risk_implication: Optional[str] = None

    message: Optional[str] = None


class PortfolioTailRiskResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int

    tail_risk_score: Optional[Decimal] = None
    worst_return_pct: Optional[Decimal] = None
    expected_shortfall_pct: Optional[Decimal] = None

    tail_risk_category: Optional[str] = None

    risk_flags: list[str] = Field(default_factory=list)

    message: Optional[str] = None


class PortfolioRecoveryAnalysisResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int

    current_drawdown_pct: Optional[Decimal] = None
    maximum_drawdown_pct: Optional[Decimal] = None

    drawdown_duration_days: Optional[int] = None

    estimated_recovery_return_pct: Optional[Decimal] = None

    recovery_status: Optional[str] = None
    recovery_category: Optional[str] = None

    risk_flags: list[str] = Field(default_factory=list)

    message: Optional[str] = None


class PortfolioRiskAlertsResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int

    alert_status: str

    alert_count: int
    critical_alert_count: int
    high_alert_count: int
    medium_alert_count: int

    alerts: list[dict] = Field(
        default_factory=list
    )

    message: Optional[str] = None


class PortfolioHealthScoreResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int

    health_score: Optional[Decimal] = None
    health_category: Optional[str] = None

    component_scores: dict = Field(
        default_factory=dict
    )

    risk_flags: list[str] = Field(
        default_factory=list
    )

    message: Optional[str] = None


class PortfolioMonitoringSummaryResponse(BaseModel):
    portfolio_id: UUID
    timeframe: str
    lookback_days: int

    monitoring_status: str

    overall_risk_score: Optional[Decimal] = None
    health_score: Optional[Decimal] = None

    current_drawdown_pct: Optional[Decimal] = None
    liquidity_score: Optional[Decimal] = None

    var_95_pct: Optional[Decimal] = None
    var_99_pct: Optional[Decimal] = None

    risk_alert_status: Optional[str] = None

    risk_alert_count: int = 0
    critical_alert_count: int = 0
    high_alert_count: int = 0
    medium_alert_count: int = 0

    risk_category: Optional[str] = None
    health_category: Optional[str] = None
    drawdown_category: Optional[str] = None
    liquidity_category: Optional[str] = None

    alerts: list[dict] = Field(
        default_factory=list
    )

    risk_flags: list[str] = Field(
        default_factory=list
    )

    message: Optional[str] = None