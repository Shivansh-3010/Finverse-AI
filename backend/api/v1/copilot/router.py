from fastapi import APIRouter

from schemas.base_response import (
    BaseResponse,
)

from services.copilot_service import (
    CopilotService,
)

router = APIRouter()


@router.get(
    "/{symbol}",
    response_model=BaseResponse
)
async def get_copilot(
    symbol: str
):

    result = (
        CopilotService.analyze(
            symbol
        )
    )

    return BaseResponse(
        success=True,
        message="Copilot analysis generated",
        data=result.model_dump()
    )