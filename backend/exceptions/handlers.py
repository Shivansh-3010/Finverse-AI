from fastapi import Request
from fastapi.responses import JSONResponse

from schemas.error_response import ErrorResponse
from core.constants import DEFAULT_ERROR_CODE


async def generic_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            message=str(exc),
            error_code=DEFAULT_ERROR_CODE
        ).model_dump()
    )