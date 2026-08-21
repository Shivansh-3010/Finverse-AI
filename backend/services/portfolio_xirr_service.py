from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from models.portfolio_transaction import TransactionType
from repositories.portfolio_transaction_repository import (
    portfolio_transaction_repository,
)
from services.portfolio_valuation_service import (
    portfolio_valuation_service,
)


def _percent(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def _xnpv(
    rate: Decimal,
    cash_flows: list[tuple[datetime, Decimal]],
) -> Decimal:
    """
    Calculate XNPV for irregularly timed cash flows.

    Cash flows:
        negative = money invested by investor
        positive = money received by investor
    """

    if not cash_flows:
        return Decimal("0")

    first_date = cash_flows[0][0]

    total = Decimal("0")

    for date, amount in cash_flows:
        days = Decimal(
            str(
                (
                    date - first_date
                ).total_seconds()
                / 86400
            )
        )

        years = days / Decimal("365")

        base = Decimal("1") + rate

        if base <= Decimal("0"):
            raise ValueError(
                "Invalid XIRR rate"
            )

        denominator = (
            base.ln() * years
        ).exp()

        total += amount / denominator

    return total


def _xirr(
    cash_flows: list[tuple[datetime, Decimal]],
) -> Decimal:
    """
    Calculate XIRR using a binary-search approach.

    Returns the annualized rate as a decimal.

    Example:
        0.12 = 12%
    """

    if len(cash_flows) < 2:
        return Decimal("0")

    has_positive = any(
        amount > Decimal("0")
        for _, amount in cash_flows
    )

    has_negative = any(
        amount < Decimal("0")
        for _, amount in cash_flows
    )

    if not has_positive or not has_negative:
        return Decimal("0")

    low = Decimal("-0.999999999999999999")
    high = Decimal("10.0")

    npv_low = _xnpv(
        low,
        cash_flows,
    )

    npv_high = _xnpv(
        high,
        cash_flows,
    )

    # Expand the upper bound when necessary.
    attempts = 0

    while (
        npv_low * npv_high > Decimal("0")
        and attempts < 20
    ):
        high *= Decimal("2")

        npv_high = _xnpv(
            high,
            cash_flows,
        )

        attempts += 1

    if npv_low * npv_high > Decimal("0"):
        return low

    for _ in range(200):

        midpoint = (
            low + high
        ) / Decimal("2")

        npv_mid = _xnpv(
            midpoint,
            cash_flows,
        )

        if abs(npv_mid) < Decimal("0.000001"):
            return midpoint

        if npv_low * npv_mid <= Decimal("0"):
            high = midpoint
            npv_high = npv_mid
        else:
            low = midpoint
            npv_low = npv_mid

    return (
        low + high
    ) / Decimal("2")


class PortfolioXIRRService:
    """
    Calculate investor-level annualized return using XIRR.

    External cash flows are treated from the investor's
    perspective:

        DEPOSIT    -> negative cash flow
        WITHDRAWAL -> positive cash flow

    The current portfolio value is treated as a positive
    terminal cash flow.
    """

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
    ) -> dict:

        transactions = (
            portfolio_transaction_repository
            .get_by_portfolio(
                db,
                portfolio_id,
            )
        )

        cash_flows: list[
            tuple[datetime, Decimal]
        ] = []

        total_deposited = Decimal("0")
        total_withdrawn = Decimal("0")

        for transaction in transactions:

            transaction_type = (
                transaction.transaction_type
            )

            amount = Decimal(
                transaction.amount
            )

            if transaction_type == (
                TransactionType.DEPOSIT.value
            ):

                total_deposited += amount

                cash_flows.append(
                    (
                        transaction.transaction_date,
                        -amount,
                    )
                )

            elif transaction_type == (
                TransactionType.WITHDRAWAL.value
            ):

                total_withdrawn += amount

                cash_flows.append(
                    (
                        transaction.transaction_date,
                        amount,
                    )
                )

        valuation_time = datetime.now(timezone.utc)

        valuation = (
            portfolio_valuation_service.calculate(
                db=db,
                portfolio_id=portfolio_id,
            )
        )

        terminal_value = Decimal(
            valuation["total_portfolio_value"]
        )

        cash_flows.append(
            (
                valuation_time,
                terminal_value,
            )
        )

        cash_flows.sort(
            key=lambda item: item[0]
        )

        xirr = _xirr(
            cash_flows
        )

        return {
            "portfolio_id": portfolio_id,

            "cash_flow_count": len(
                cash_flows
            ),

            "total_deposited": _money(
                total_deposited
            ),

            "total_withdrawn": _money(
                total_withdrawn
            ),

            "terminal_value": _money(
                terminal_value
            ),

            "xirr": _percent(
                xirr
            ),

            "xirr_pct": _percent(
                xirr * Decimal("100")
            ),

            "cash_flows": [
                {
                    "date": date,
                    "amount": amount,
                }
                for date, amount in cash_flows
            ],
        }


def _money(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


portfolio_xirr_service = PortfolioXIRRService()