from fastapi import APIRouter

from schemas.base_response import BaseResponse

router = APIRouter()


@router.get("/", response_model=BaseResponse)
async def get_stocks():
    return BaseResponse(
        success=True,
        message="Stocks endpoint ready",
        data={}
    )