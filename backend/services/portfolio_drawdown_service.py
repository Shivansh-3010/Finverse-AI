from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from repositories.ohlcv_repository import OHLCVRepository
from services.holding_service import holding_service


def _round(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioDrawdownService:
    """
    Calculates historical portfolio drawdown analytics.

    Metrics:
        - Current drawdown
        - Maximum drawdown
        - Peak portfolio value
        - Current portfolio value
        - Drawdown duration
        - Recovery status
        - Recovery time
    """

    def __init__(self) -> None:
        self.ohlcv_repository = OHLCVRepository

    def _portfolio_history(
        self,
        db: Session,
        portfolio_id: UUID,
        timeframe: str,
        lookback_days: int,
    ) -> list[dict]:

        holdings = holding_service.calculate_from_transactions(
            db,
            portfolio_id,
        )

        if not holdings:
            return []

        end = datetime.now(timezone.utc)
        start = end - timedelta(days=lookback_days)

        prices_by_symbol = {}

        for holding in holdings:
            symbol = holding["symbol"]

            rows = (
                self.ohlcv_repository(db)
                .get_history_by_symbol_and_timeframe_between(
                    symbol,
                    timeframe,
                    start,
                    end,
                )
            )

            if rows:
                prices_by_symbol[symbol] = {
                    row.timestamp: Decimal(str(row.close))
                    for row in rows
                    if row.close is not None
                }

        if not prices_by_symbol:
            return []

        common_dates = None

        for prices in prices_by_symbol.values():

            dates = set(prices.keys())

            if common_dates is None:
                common_dates = dates
            else:
                common_dates &= dates

        if not common_dates:
            return []

        dates = sorted(common_dates)

        weights = {
            holding["symbol"]: Decimal(
                str(holding["cost_basis"])
            )
            for holding in holdings
            if holding["symbol"] in prices_by_symbol
        }

        total_weight = sum(
            weights.values(),
            Decimal("0"),
        )

        if total_weight <= Decimal("0"):
            return []

        normalized_weights = {
            symbol: weight / total_weight
            for symbol, weight in weights.items()
        }

        history = []

        for date in dates:

            portfolio_value = Decimal("0")

            for symbol, weight in normalized_weights.items():
                portfolio_value += (
                    prices_by_symbol[symbol][date]
                    * weight
                )

            history.append(
                {
                    "timestamp": date,
                    "value": portfolio_value,
                }
            )

        return history

    def calculate(
        self,
        db: Session,
        portfolio_id: UUID,
        timeframe: str = "1d",
        lookback_days: int = 30,
    ) -> dict:

        history = self._portfolio_history(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
            lookback_days=lookback_days,
        )

        base_response = {
            "portfolio_id": portfolio_id,
            "timeframe": timeframe,
            "lookback_days": lookback_days,
        }

        if len(history) < 2:

            return {
                **base_response,
                "observation_count": len(history),
                "current_portfolio_value": None,
                "peak_portfolio_value": None,
                "current_drawdown_pct": None,
                "maximum_drawdown_pct": None,
                "drawdown_duration_days": None,
                "recovery_status": "Insufficient Data",
                "recovery_time_days": None,
                "drawdown_category": "Insufficient Data",
                "risk_flags": [
                    "Insufficient portfolio history"
                ],
                "message": "Insufficient portfolio history",
            }

        peak_value = Decimal("0")
        peak_timestamp = None

        maximum_drawdown = Decimal("0")
        maximum_drawdown_timestamp = None

        current_value = history[-1]["value"]

        current_peak_timestamp = None

        for item in history:

            value = item["value"]

            if value > peak_value:
                peak_value = value
                peak_timestamp = item["timestamp"]
                current_peak_timestamp = item["timestamp"]

            if peak_value > Decimal("0"):

                drawdown = (
                    (
                        value - peak_value
                    )
                    / peak_value
                ) * Decimal("100")

                if drawdown < maximum_drawdown:
                    maximum_drawdown = drawdown
                    maximum_drawdown_timestamp = (
                        item["timestamp"]
                    )

        current_drawdown = Decimal("0")

        if peak_value > Decimal("0"):

            current_drawdown = (
                (
                    current_value - peak_value
                )
                / peak_value
            ) * Decimal("100")

        current_drawdown = _round(
            current_drawdown
        )

        maximum_drawdown = _round(
            maximum_drawdown
        )

        recovery_status = "At Peak"
        recovery_time_days = None

        if current_value < peak_value:

            recovery_status = "In Drawdown"

        elif (
            maximum_drawdown < Decimal("0")
            and peak_timestamp is not None
        ):

            recovery_status = "Recovered"

            recovery_time_days = (
                history[-1]["timestamp"]
                - peak_timestamp
            ).days

        drawdown_duration_days = 0

        if current_drawdown < Decimal("0"):

            if current_peak_timestamp is not None:

                drawdown_duration_days = (
                    history[-1]["timestamp"]
                    - current_peak_timestamp
                ).days

        drawdown_duration_days = max(
            0,
            drawdown_duration_days,
        )

        absolute_drawdown = abs(
            maximum_drawdown
        )

        if absolute_drawdown >= Decimal("30"):

            drawdown_category = "Severe Drawdown"

        elif absolute_drawdown >= Decimal("20"):

            drawdown_category = "High Drawdown"

        elif absolute_drawdown >= Decimal("10"):

            drawdown_category = "Moderate Drawdown"

        elif absolute_drawdown > Decimal("0"):

            drawdown_category = "Low Drawdown"

        else:

            drawdown_category = "No Drawdown"

        risk_flags = []

        if abs(current_drawdown) >= Decimal("20"):

            risk_flags.append(
                "Portfolio is currently experiencing a severe drawdown"
            )

        elif abs(current_drawdown) >= Decimal("10"):

            risk_flags.append(
                "Portfolio is currently experiencing a significant drawdown"
            )

        if absolute_drawdown >= Decimal("20"):

            risk_flags.append(
                "Historical maximum drawdown exceeds 20%"
            )

        if (
            drawdown_duration_days >= 30
            and current_drawdown < Decimal("0")
        ):

            risk_flags.append(
                "Portfolio has remained in drawdown for an extended period"
            )

        if not risk_flags:

            risk_flags.append(
                "No major drawdown risks detected"
            )

        return {
            **base_response,
            "observation_count": len(history),
            "current_portfolio_value": _round(
                current_value
            ),
            "peak_portfolio_value": _round(
                peak_value
            ),
            "current_drawdown_pct": current_drawdown,
            "maximum_drawdown_pct": maximum_drawdown,
            "drawdown_duration_days": drawdown_duration_days,
            "recovery_status": recovery_status,
            "recovery_time_days": recovery_time_days,
            "drawdown_category": drawdown_category,
            "risk_flags": risk_flags,
            "message": None,
        }


portfolio_drawdown_service = (
    PortfolioDrawdownService()
)