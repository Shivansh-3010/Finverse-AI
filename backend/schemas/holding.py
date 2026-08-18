from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HoldingCreate(BaseModel):
    portfolio_id: UUID
    symbol: str = Field(
        min_length=1,
        max_length=20,
    )
    quantity: Decimal
    avg_price: Decimal
    current_price: Decimal
    market_value: Decimal


class HoldingResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    portfolio_id: UUID
    symbol: str
    quantity: Decimal
    avg_price: Decimal
    current_price: Decimal
    market_value: Decimal
    created_at: datetime
    updated_at: datetime