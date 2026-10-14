from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from models.portfolio_transaction import TransactionType
from repositories.portfolio_snapshot_repository import (
    portfolio_snapshot_repository,
)
from repositories.portfolio_transaction_repository import (
    portfolio_transaction_repository,
)


def _percent(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioTWRService:
    """
    Calculate portfolio Time-Weighted Return (TWR).

    TWR removes the effect of external cash flows by
    calculating returns for individual sub-periods and
    geometrically linking those returns.

    External cash flows are deposits and withdrawals only.
    """

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
    ) -> dict:

        snapshots = (
            portfolio_snapshot_repository.get_by_portfolio(
                db,
                portfolio_id,
            )
        )

        if len(snapshots) < 2:
            return {
                "portfolio_id": portfolio_id,
                "snapshot_count": len(snapshots),
                "period_count": 0,
                "twr": Decimal("0.00"),
                "twr_pct": Decimal("0.00"),
                "periods": [],
            }

        transactions = (
            portfolio_transaction_repository.get_by_portfolio(
                db,
                portfolio_id,
            )
        )

        periods = []
        linked_return = Decimal("1")

        transaction_index = 0

        for index in range(1, len(snapshots)):
            previous = snapshots[index - 1]
            current = snapshots[index]

            beginning_value = Decimal(previous.portfolio_value)
            ending_value = Decimal(current.portfolio_value)
            cash_flow = Decimal("0")

            # Transactions are returned in ascending transaction_date order.
            # Advance past transactions that belong before this sub-period.
            while (
                transaction_index < len(transactions)
                and transactions[transaction_index].transaction_date
                <= previous.snapshot_time
            ):
                transaction_index += 1

            # Process only transactions inside the current sub-period.
            while (
                transaction_index < len(transactions)
                and transactions[transaction_index].transaction_date
                <= current.snapshot_time
            ):
                transaction = transactions[transaction_index]

                if transaction.transaction_type == TransactionType.DEPOSIT.value:
                    cash_flow += Decimal(transaction.amount)

                elif transaction.transaction_type == TransactionType.WITHDRAWAL.value:
                    cash_flow -= Decimal(transaction.amount)

                transaction_index += 1

            adjusted_beginning_value = beginning_value + cash_flow

            if adjusted_beginning_value <= Decimal("0"):
                period_return = Decimal("0")
            else:
                period_return = (
                    ending_value / adjusted_beginning_value
                ) - Decimal("1")

            linked_return *= Decimal("1") + period_return

            periods.append({
                "start": previous.snapshot_time,
                "end": current.snapshot_time,
                "beginning_value": beginning_value,
                "cash_flow": cash_flow,
                "ending_value": ending_value,
                "return": _percent(period_return * Decimal("100")),
            })
        twr = linked_return - Decimal("1")

        return {
            "portfolio_id": portfolio_id,
            "snapshot_count": len(snapshots),
            "period_count": len(periods),
            "twr": _percent(
                twr * Decimal("100")
            ),
            "twr_pct": _percent(
                twr * Decimal("100")
            ),
            "periods": periods,
        }


portfolio_twr_service = PortfolioTWRService()