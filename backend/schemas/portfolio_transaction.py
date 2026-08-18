from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PortfolioTransactionCreate(BaseModel):
    portfolio_id: UUID
    symbol: str = Field(
        min_length=1,
        max_length=20,
    )
    transaction_type: str = Field(
        min_length=1,
        max_length=20,
    )
    quantity: Decimal | None = None
    price: Decimal | None = None
    amount: Decimal
    transaction_date: datetime
    reference: str | None = Field(
        default=None,
        max_length=255,
    )


class PortfolioTransactionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    portfolio_id: UUID
    symbol: str
    transaction_type: str
    quantity: Decimal | None
    price: Decimal | None
    amount: Decimal
    transaction_date: datetime
    reference: str | None
    created_at: datetime
    updated_at: datetime