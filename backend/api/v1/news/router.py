from fastapi import APIRouter

from schemas.base_response import BaseResponse

router = APIRouter()


@router.get("/", response_model=BaseResponse)
async def get_news():
    return BaseResponse(
        success=True,
        message="News endpoint ready",
        data={}
    )