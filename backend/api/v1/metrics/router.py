from fastapi import APIRouter

from schemas.base_response import (
    BaseResponse,
)

from metrics.monitoring_metrics import (
    MonitoringMetrics,
)

router = APIRouter()


@router.get(
    "/",
    response_model=BaseResponse
)
async def get_metrics():

    return BaseResponse(
        success=True,
        message="Monitoring metrics",
        data=MonitoringMetrics.get_metrics()
    )