from fastapi import APIRouter

from schemas.base_response import BaseResponse

router = APIRouter()


@router.get("/", response_model=BaseResponse)
async def health_check():
    return BaseResponse(
        success=True,
        message="Health check successful",
        data={
            "status": "healthy",
            "postgres": "configured",
            "redis": "configured",
            "chromadb": "configured"
        }
    )
    
