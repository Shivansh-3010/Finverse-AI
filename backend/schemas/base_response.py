from pydantic import BaseModel
from typing import Any


class BaseResponse(BaseModel):
    success: bool
    message: str
    data: Any | None = None